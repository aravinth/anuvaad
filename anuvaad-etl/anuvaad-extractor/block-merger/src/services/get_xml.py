import os
import uuid 
import config
import logging
import time
import pandas as pd
from anuvaad_auditor.loghandler import log_info
from anuvaad_auditor.loghandler import log_error

from src.utilities.xml_utils import ( get_string_xmltree, get_xmltree, get_specific_tags, get_page_texts_ordered, get_page_text_element_attrib, get_ngram)
from src.services.xml_document_info import (get_xml_info, get_xml_image_info, get_pdf_image_info)
from src.utilities.filesystem import (create_directory,extract_image_paths_from_pdf, extract_html_bg_image_paths_from_digital_pdf, extract_xml_path_from_digital_pdf)

from src.services.box_horizontal_operations import (merge_horizontal_blocks)
from src.services.box_vertical_operations import (merge_vertical_blocks)
from src.services.preprocess import  tag_heaader_footer_attrib
from src.services.left_right_on_block import left_right_margin
import src.utilities.app_context as app_context


def create_pdf_processing_paths(filename, base_dir):
    data_dir    = os.path.join(base_dir, 'data')
    ret         = create_directory(data_dir)

    if ret == False:
        log_error('unable to create data directory {}'.format(data_dir), app_context.application_context, None)
        return False
    
    output_dir  = os.path.join(data_dir, 'output')
    ret         = create_directory(output_dir)
    if ret == False:
        log_error('unable to create output directory {}'.format(output_dir), app_context.application_context, None)
        return False

    working_dir = os.path.join(output_dir, os.path.splitext(filename)[0]+'_'+str(uuid.uuid1()))
    ret         = create_directory(working_dir)
    if ret == False:
        log_error('unable to create working directory {}'.format(working_dir), app_context.application_context, None)
        return False
    
    log_info('created processing directories successfully', app_context.application_context)
    
    return working_dir, True

def extract_pdf_metadata(filename, working_dir, base_dir):
    start_time          = time.time()
    pdf_filepath        = os.path.join(base_dir, filename)

    try:
        pdf_image_paths         = extract_image_paths_from_pdf(pdf_filepath, working_dir)
        pdf_xml_filepath        = extract_xml_path_from_digital_pdf(pdf_filepath, working_dir)
    except Exception as e:
        log_error('error extracting xml information of {}'.format(pdf_filepath)+e, app_context.application_context, e)
        return None, None, None
    log_info('Extracting xml of {}'.format(pdf_filepath), app_context.application_context)
    
    try:
        pdf_bg_img_filepaths    = extract_html_bg_image_paths_from_digital_pdf(pdf_filepath, working_dir)
    except Exception as e:
        log_error('unable to extract background images of {}'.format(pdf_filepath), app_context.application_context, None)
        return None, None, None

    log_info('Extracting background images of {}'.format(pdf_filepath), app_context.application_context)

    end_time            = time.time()
    extraction_time     = end_time - start_time
    log_info('Extraction of {} completed in {}'.format(pdf_filepath, extraction_time), app_context.application_context)
    
    return pdf_xml_filepath, pdf_image_paths, pdf_bg_img_filepaths

def process_input_pdf(filename, base_dir, lang):
    '''
        - from the input extract following details
            - xml
            - images present in xml
            - background image present in each page
    '''
    working_dir, ret = create_pdf_processing_paths(filename, base_dir)
    
    if ret == False:
        log_error('create_pdf_processing_paths failed', app_context.application_context, None)
        return None, None, None, None, None, None, None
    
    pdf_xml_filepath, pdf_image_paths, pdf_bg_img_filepaths   = extract_pdf_metadata(filename, working_dir, base_dir)
    if pdf_xml_filepath == None or pdf_bg_img_filepaths == None:
        log_error('extract_pdf_metadata failed', app_context.application_context, None)
        return None, None, None, None, None, None, None

    '''
        - parse xml to create df per page for text and table block.
        - parse xml to create df per page for image block.
    '''
    try :
        xml_dfs, page_width, page_height = get_xml_info(pdf_xml_filepath, lang)
    except Exception as e :
        log_error('get_xml_info failed'+e, app_context.application_context, e)
        return None, None, None, None, None, None, None

    try :
        img_dfs, page_width, page_height = get_xml_image_info(pdf_xml_filepath)
    except Exception as e :
        log_error('Error in extracting image xml info failed', app_context.application_context, e)
        return None, None, None, None, None, None, None

    log_info('process_input_pdf: created dataframes successfully', app_context.application_context)
    return img_dfs, xml_dfs, page_width, page_height, working_dir, pdf_bg_img_filepaths, pdf_image_paths

    
def get_vdfs(h_dfs):
    start_time          = time.time()
    document_configs    = config.DOCUMENT_CONFIGS
    v_dfs = []
    pages = len(h_dfs)
    try :
        for page_index in range(pages):
            h_df    = h_dfs[page_index]
            v_df    = merge_vertical_blocks(h_df, document_configs, debug=False)
            v_dfs.append(v_df)
    except Exception as e :
        log_error('Error in creating v_dfs', app_context.application_context, e)
        return None

    end_time            = time.time()
    extraction_time     = end_time - start_time
    log_info('Extraction of v_dfs completed in {}'.format(extraction_time), app_context.application_context)

    return v_dfs

        
def get_hdfs(in_dfs,header_region , footer_region):
    
    start_time          = time.time()
    pages = len(in_dfs)
    multiple_pages = False
    if pages > 1:
        multiple_pages =True
    h_dfs = []
    document_configs = config.DOCUMENT_CONFIGS
    try:
        for page_index in range(pages):
            page_df   = in_dfs[page_index]
            page_df   = page_df.loc[:]
            if multiple_pages :
                page_df   = tag_heaader_footer_attrib(header_region , footer_region,page_df)

        
            h_df    = merge_horizontal_blocks(page_df, document_configs, debug=False)
            h_dfs.append(h_df)
    except Exception as e :

        #print(e)
        log_error('Error in creating h_dfs', app_context.application_context, e)
        log_error(e, app_context.application_context, e)
        return None

    end_time            = time.time()
    extraction_time     = end_time - start_time
    log_info('Extraction of h_dfs completed in {}'.format(extraction_time), app_context.application_context)

    return h_dfs



def get_pdfs(page_dfs):
    start_time          = time.time()
    p_dfs    = []
    pages    = len(page_dfs)
    block_configs = config.BLOCK_CONFIGS
    try :
        for page_index in range(pages):
            page_df     = page_dfs[page_index]
            cols        = page_df.columns.values.tolist()
            df          = pd.DataFrame(columns=cols)
            
            for index, row in page_df.iterrows():

                if row['children'] == None:
                    d_tmp = page_df.iloc[index]
                    d_tmp['avg_line_height'] = int(d_tmp['text_height'])
                    
                    df = df.append(d_tmp)
                else:
                    dfs = process_block(page_df.iloc[index], block_configs)
                    df  = df.append(dfs)

            
            p_dfs.append(df)
    except Exception as e :
        log_error('Error in creating p_dfs', app_context.application_context, e)
        return None

    end_time            = time.time()
    extraction_time     = end_time - start_time
    log_info('Extraction of p_dfs completed in {}'.format(extraction_time), app_context.application_context)
    return p_dfs


def process_block(children, block_configs):
    dfs = left_right_margin(children, block_configs)
    return dfs


def drop_cols(df,drop_col=None ):
    if drop_col==None:
        drop_col = ['index', 'xml_index','level_0']
    
    for col in drop_col:
        if col in df.columns:
            df = df.drop(columns=[col])
    return df

def change_font(font_name):
    if '+' in font_name:
        font = font_name.split('+')[1]
    else:
        font = font_name
    return font

def page_font_update(page_df):
    
    page_df     = page_df.where(page_df.notnull(), None)
    for index, row in page_df.iterrows():
        page_df.at[index,'font_family'] = change_font(row["font_family"])
        if 'children' in page_df.columns:
            if row['children'] == None:
                pass
            else:
                sub_block_children   =  pd.read_json(row['children'])
                df = page_font_update(sub_block_children)
                page_df.at[index,'children'] = df.to_json()
                
    return page_df

def update_font(p_dfs):
    start_time          = time.time()
    pages    = len(p_dfs)
    new_dfs  = []
    try:
        for page_index in range(pages):

            page_df     = p_dfs[page_index]
            
            page_lis    = []
            child_lis   = []
            df = page_font_update(page_df)
            new_dfs.append(df)
    except Exception as e :
        log_error('Error in updating fonts', app_context.application_context, e)
        return None
    end_time            = time.time()
    extraction_time     = end_time - start_time
    log_info('Updating of fonts completed in {}'.format(extraction_time), app_context.application_context)
    return new_dfs
  
    

    
                
                        