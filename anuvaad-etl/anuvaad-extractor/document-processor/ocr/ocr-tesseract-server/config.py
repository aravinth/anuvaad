import os
import time
DEBUG = False
API_URL_PREFIX = "/anuvaad-etl/document-processor/tesseract-document-digitization"
HOST = '0.0.0.0'
PORT = 5001
BASE_DIR = 'upload'
#BASE_DIR      = '/home/naresh/anuvaad/anuvaad-etl/anuvaad-extractor/document-processor/ocr/ocr-tesseract-server/'
download_folder = 'upload'

# os.environ['OMP_THREAD_LIMIT']='1'

ENABLE_CORS = False

# kafka

# ENABLE_CORS = False

# # kafka

input_topic_default = 'anuvaad-dp-tools-ocr-tesseract-input-v20'
input_topic_identifier = 'KAFKA_ANUVAAD_DP_TOOLS_OCR_TESSERACT_INPUT_V20'
input_topic = os.environ.get(input_topic_identifier, input_topic_default)

output_topic_default = 'anuvaad-dp-tools-ocr-tesseract-output-v20'
output_topic_identifier = 'KAFKA_ANUVAAD_DP_TOOLS_OCR_TESSERACT_OUTPUT_V20'
output_topic = os.environ.get(output_topic_identifier, output_topic_default)

kf_local_server = 'localhost:9092'
kafka_ip_host = 'KAFKA_BOOTSTRAP_SERVER_HOST'
bootstrap_server = os.environ.get(kafka_ip_host, kf_local_server)

TASK_STAT = 'TESSERACT-OCR-20'

CONSUMER_GROUP_default = 'anuvaad-etl-tesseractocr-20-consumer-group'
CONSUMER_GROUP_identifier = 'ANUVAAD_ETL_TESSERACTOCR_CONSUMER_GROUP_V20'
CONSUMER_GROUP = os.environ.get(
    CONSUMER_GROUP_identifier, CONSUMER_GROUP_default)
download_folder = 'upload'

SAVE_VAR = "OCR_CH_URL"
SAVE_DEFAULT = "http://gateway_anuvaad-ocr-content-handler:5001//anuvaad/ocr-content-handler/v0/ocr/save-document"

SAVE_URL = os.environ.get(SAVE_VAR, SAVE_DEFAULT)
SAVE_NO_PAGE = 1

IS_DYNAMIC = False
EXRACTION_RESOLUTION = 300
BATCH_SIZE = 1
DYNAMIC_MARGINS = False
PERSPECTIVE_TRANSFORM = True
FALL_BACK_LANGUAGE = None
PSM = 7
POST_PROCESSING_MODE = None
MULTIPROCESS = False
DOUBLE_OCR_THRESHOLD = 20

# crop config
C_X = -7
C_Y = 0

HORIZONTAL_MERGING=True

LANG_MAPPING       =  {
    "en" : ["Latin","eng"],
    "kn" : ['Kannada',"kan"],
    "gu": ["guj"],
    "or": ["ori"],
    "hi" : ["Devanagari","hin","eng"],
    "bn" : ["Bengali","ben"],
    "mr": ["Devanagari","hin","eng"],
    "ta": ['Tamil',"tam"],
    "te" : ["Telugu","tel"],
    "ml" :["Malayalam"],
    "ur" :["Arabic", "Urdu"],
    "pa" :["Gurmukhi","pan"],
    "ne" :["nep","Nepali"],
    "brx" :["Devanagari","bod", "Bodo", "boro"],
    "as" :["asm"],
    "sa" :["san"],
    "ks" :["Arabic"],
    "ks_Deva" :["Devanagari"],
    "gom":["Devanagari"],
    "mni":["Devanagari"],
    "mni_Beng":["Bengali"],
    "mai":["Devanagari"],
    "sd_Deva" :["Arabic"],
    "sd" :["sin"],
    "doi":["Devanagari"]
}

DETECT_LANG_MAPPING = {
    "Latin": ["Latin"],
    "Kannada": ['anuvaad_kan'],
    "Gujrati": ["guj"],
    "Oriya": ["anuvaad_ori"],
    "Devanagari": ["anuvaad_hin"],
    "Bengali": ["anuvaad_ben"],
    "Tamil": ['anuvaad_tam'],
    "Telugu": ["Telugu"],
    "Malayalam": ["anuvaad_mal"],
    "Marathi": ["anuvaad_mar"],
    "Punjabi": ["Gurmukhi"],
    "Santali":["san"]

}

TESS_LANG_MAPPING = {
    "en": ['Latin'],
    "kn": ['anuvaad_kan'],
    "gu": ['guj'],
    "or": ['anuvaad_ori'],
    "hi": ['anuvaad_hin'],
    "bn": ['anuvaad_ben'],
    "mr": ['anuvaad_hin'],
    "ta": ['anuvaad_tam'],
    "te": ['Telugu'],
    "ml": ['anuvaad_mal'],
    "ma": ['anuvaad_mar'],  
    "pa": ['Gurmukhi']  
}
