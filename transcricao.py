import whisper
import streamlit as st
import os

#CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title='Transcrição')

hide_menu = """<style>
#MainMenu{
    visibility:hidden;
}
footer{
    visibility:hidden;
}
</style>"""
#CONFIGURAÇÕES DA PÁGINA

#def clean_folder():
#    files = []
#    now = time.time()
#
#    for file in os.listdir():
#        if file == os.path.basename(__file__):
#            continue
#        elif os.stat(file).st_mtime < now - 5 and os.path.isfile(file):
#            os.remove(file)
#
#clean_folder()

resultado = ''

if 'text_box' not in st.session_state:
    st.session_state['text_box'] = ''

st.markdown(hide_menu, unsafe_allow_html=True)
st.title('Transcrição')
st.caption('Efetue trancrições facilmente :sunglasses:')
st.caption('\n')

text_box = ''
devices = "cuda" 

uploaded_file = st.file_uploader("1 - Selecione o arquivo para transcrição", type=['mp3', 'wav', 'ogg', 'aac'])
if uploaded_file is not None:
    with open(os.path.join(os.getcwd(),uploaded_file.name),"wb") as f: 
      f.write(uploaded_file.getbuffer()) 
      text_box = f'{uploaded_file.name}'

def Transcrever(): 
    del st.session_state['text_box'] 
    global resultado
    model = whisper.load_model(mode, device=devices)
    result = model.transcribe(uploaded_file.name, fp16=False)
    st.session_state['text_box'] = result['text'].strip()
    os.remove(text_box)

def Limpar(): 
    del st.session_state['text_box']
    pass

modes =  {'large': "Lento (alta qualidade)", 'medium': "Mediano (qualidade mediana)", 'small': "Rápido (qualidade intermediária)", 'base': "Extremamente rápido (baixa qualidade)"}

def format_func(option):
    return modes[option] 

mode = st.selectbox("2 - Selecione a categoria da transcrição e clique em transcrever", options=list(modes.keys()), format_func=format_func)
if uploaded_file == None:
    st.button('Transcrever', disabled=True)
else:
    st.button('Transcrever', disabled=False, on_click=Transcrever)

st.text_area('Texto pós-transcrição', value=st.session_state['text_box'], key='text_box', disabled=True)

with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    if st.session_state['text_box'] == '':
        col1.button('Limpar transcrição', on_click=Limpar, disabled=True)
    else:
        col1.button('Limpar transcrição', on_click=Limpar, disabled=False)
        
    if st.session_state['text_box'] == '':
        col6.download_button(label="Download Transcrição",data=st.session_state['text_box'],file_name='transcrição.txt',mime="text/plain", disabled=True)
    else:
        col6.download_button(label="Download Transcrição",data=st.session_state['text_box'],file_name=f'{uploaded_file.name}.txt',mime="text/plain", disabled=False)
