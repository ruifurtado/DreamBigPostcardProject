from os import walk, getcwd
from PIL import ImageOps, Image, ImageFont, ImageDraw
from pathlib import Path

import streamlit as st

st.set_page_config(page_icon="✌️", page_title="Postcard editor")

A4_WIDTH = 3508
A4_HEIGHT = 2480 
MARGIN_WIDTH = 90
MARGIN_HEIGHT = 125

DRAW_TUPLE = (int(A4_WIDTH/4)-MARGIN_WIDTH,int(A4_HEIGHT/4)-MARGIN_HEIGHT)
LAYOUT_TUPLE = (int(A4_WIDTH/4), (int(A4_HEIGHT/4)))

DOWN_CENTER_TITLE = ((A4_WIDTH/4)/2, ((A4_HEIGHT/4)/2)+265)
DOWN_CENTER_SUBTITLE = ((A4_WIDTH/4)/2, ((A4_HEIGHT/4)/2)+292)

zoom_map = {
    "1 px":1,
    "1.1 px":1.1,
    "1.2 px":1.2,
    "1.3 px":1.3,
    "1.4 px":1.4,
    "1.5 px":1.5,
    "1.75 px":1.75,
    "2 px":2
}

def postcard_creator(filenames:list,fonts:list):
    """
    Postcard front page creator
    """

    # Title
    st.title("Front page")

    # Front page
    st.sidebar.title('Front page')

    # Select desired image
    image_name = st.sidebar.selectbox(
        label = "Select your image",
        options = filenames,
        index = 1
    )
    image = Image.open(f'Draws/{image_name}.jpg')
    im = image.resize(DRAW_TUPLE)

    # Zoom in the image
    zoom = st.sidebar.selectbox(
        label = "Select zoom",
        options = zoom_map.keys(),
        index=0
    )

    zoom = zoom_map[zoom]
    im = im.crop((((im.size[0]/2)-im.size[0]/(zoom*2)),((im.size[1]/2)-im.size[1]/(zoom*2)),((im.size[0]/2)+im.size[0]/(zoom*2)),((im.size[1]/2)+im.size[1]/(zoom*2))))
    im = im.resize(DRAW_TUPLE)

    # Select desired layout color 
    layout_color = st.sidebar.color_picker(
        label = "Select margin color",
        value = '#ffffff' 
    )

    layout = Image.new('RGB', LAYOUT_TUPLE, layout_color)
    box = tuple((n - o) // 2 for n, o in zip(LAYOUT_TUPLE,DRAW_TUPLE))
    layout.paste(im, box)
    
    image_draw = ImageDraw.Draw(layout)

    # Select title font
    title_font_name = st.sidebar.selectbox(
        label = "Select title font",
        options = fonts,
        index = 16
    )
    # Font for first image
    title_font = ImageFont.truetype(f'Fonts/{title_font_name}', 27)

    #Select title text
    title_text = st.sidebar.text_input(
        label="Select postcard title",
        value="Cristina School"
    )

    # Select title color 
    title_color = st.sidebar.color_picker(
        label = "Select title color",
        value = '#DBC759' 
    )

    title_loc = DOWN_CENTER_TITLE
    image_draw.text(
        title_loc, 
        title_text, 
        font=title_font, 
        fill=title_color, 
        align='center', 
        anchor="mm"
    )

    # Subtitle font name
    subtitle_font_name = st.sidebar.selectbox(
        label = "Select subtitle font",
        options = fonts,
        index = 23
    )

    # Subtitle font
    subtitle_font = ImageFont.truetype(f'Fonts/{subtitle_font_name}', 18)

    #Select subtitle text
    subtitle_text = st.sidebar.text_input(
        label="Select postcard subtitle",
        value="Prasat Bakong"
    )

    # Select subtitle color 
    subtitle_color = st.sidebar.color_picker(
        label = "Select subtitle color",
        value = '#000000' 
    )

    subtitle_loc = DOWN_CENTER_SUBTITLE
    image_draw.text(
        subtitle_loc, 
        subtitle_text, 
        font=subtitle_font, 
        fill=subtitle_color, 
        align='center', 
        anchor="mm"
    )
    
    st.sidebar.write("Filters")

    if st.sidebar.checkbox(label="invert colors"):
        layout_invert = ImageOps.invert(layout)
        layout = layout_invert
    
    if st.sidebar.checkbox(label="solarize"):
        layout_solar = ImageOps.solarize(layout)
        layout = layout_solar
    
    st.image(layout)
    return

def back_page_selector(backpages:list):
    """
    Postcard back page selector
    """
    
    # Title 
    st.title('Back Page')

    # Title on sidebar
    st.sidebar.title("Back Page")
    
    # Select back page image
    backpage_name = st.sidebar.selectbox(
        label = "select backpage layout",
        options = backpages,
        index = 0
    )

    backpage_img = Image.open(f'Back/{backpage_name}.jpg')
    backpage = backpage_img.resize(LAYOUT_TUPLE)

    st.image(backpage)
    return

def main():
    st.write(f'{getcwd()}/Logo/Cambodia_button_go-1.png')
    st.sidebar.image(f'{getcwd()}/Logo/Cambodia_button_go-1.png')
    st.sidebar.title("Description")
    st.sidebar.write("On this sidebar you can edit each postcard looks by changing it's different componets")
        
    filenames = next(walk("Draws"), (None, None, []))[2]  # [] if no file
    filenames = [filename.split('.jpg')[0] for filename in filenames]

    fonts = next(walk("Fonts"), (None, None, []))[2]  # [] if no file
    fonts = [font.split('.jpg')[0] for font in fonts]

    backpages = next(walk("Back"), (None, None, []))[2]
    backpages = [back.split('.jpg')[0] for back in backpages]

    postcard_creator(
        filenames=filenames,
        fonts=fonts
    )

    back_page_selector(
        backpages=backpages
    )
    return

st.image("Logo\dreambig_logo_A_main-1.png")
st.write(
    "bla bla bla bla explain the project here..............."
)



main()
