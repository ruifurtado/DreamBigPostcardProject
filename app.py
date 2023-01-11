from os import walk
from PIL import ImageOps, Image, ImageFont, ImageDraw
from io import BytesIO

import os
import numpy
import streamlit as st

st.set_page_config(page_icon="✌️", page_title="Postcard editor")

A4_WIDTH = 3508
A4_HEIGHT = 2480 
BACKGROUND_TUPLE = (int(A4_WIDTH/4), (int(A4_HEIGHT/4)))

LAYOUTS = {
    'layout 1':{
        "DRAW_TUPLE":(int(A4_WIDTH/4)-80,int(A4_HEIGHT/4)-113), # Position of the draw
        "BOX_CORRECTION":(0,-9), # correction from the center (the image is placed on the center of the background)
        "TITLE_SIZE":27,
        "TITLE":{
            "center": ((A4_WIDTH/4)/2, ((A4_HEIGHT/4)/2)+263), # center
            'left':(127, ((A4_HEIGHT/4)/2)+263), # left
            "right": (750, ((A4_HEIGHT/4)/2)+263), # right
        },
        "SUBTITLE_SIZE":20,
        "SUBTITLE":{
            "center": ((A4_WIDTH/4)/2, ((A4_HEIGHT/4)/2)+290), # center
            'left':(97, ((A4_HEIGHT/4)/2)+290), # left
            "right":(780, ((A4_HEIGHT/4)/2)+290), # right
        }
    },
    'layout 2':{
        "DRAW_TUPLE":(int(A4_WIDTH/4)-105,int(A4_HEIGHT/4)-65), # Position of the draw
        "BOX_CORRECTION":(0,-9), # correction from the center (the image is placed on the center of the background)
        "TITLE_SIZE":31,
        "SUBTITLE1_SIZE":18,
        "SUBTITLE2_SIZE":18
    }
}

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

def append_images(images, direction='horizontal',
                  bg_color=(255,255,255), aligment='center'):
    """
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: white)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """
    widths, heights = zip(*(i.size for i in images))

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)

    new_im = Image.new('RGB', (new_width, new_height), color=bg_color)


    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im

def postcard_creator():
    """
    Postcard front page creator
    """

    # Title
    st.title("Front page")

    # Description
    st.markdown(
        "- ##### Here you can visualize how the layout changes affect the postcard's frontpage"  
    )

    # Sidebar title
    st.sidebar.title('Front page')

    # Upload frontpage file
    file = st.sidebar.file_uploader(
        label="Upload frontpage image",
        type = ['png', 'jpg','jpeg']
    )
    if file: save_in_folder('Draws',file)

    # Select desired image
    image_name = st.sidebar.selectbox(
        label = "Select your image",
        options = files_in_folder('Draws'),
        index = 1
    )

    # Select layout
    layout_name = st.sidebar.selectbox(
        label = "Select margin layout",
        options = LAYOUTS.keys(),
        index=0
    )

    # Get image and resize for A4/4 size
    image = Image.open(f'Draws/{image_name}')
    im = image.resize(LAYOUTS[layout_name]['DRAW_TUPLE'])

    # Zoom in the image
    zoom = st.sidebar.selectbox(
        label = "Select zoom",
        options = zoom_map.keys(),
        index=0
    )
    zoom = zoom_map[zoom]
    im = im.crop((((im.size[0]/2)-im.size[0]/(zoom*2)),((im.size[1]/2)-im.size[1]/(zoom*2)),((im.size[0]/2)+im.size[0]/(zoom*2)),((im.size[1]/2)+im.size[1]/(zoom*2))))
    im = im.resize(LAYOUTS[layout_name]['DRAW_TUPLE'])

    # Select desired margin color 
    margin_color = st.sidebar.color_picker(
        label = "Select margin color",
        value = '#ffffff' 
    )

    # margin plus selected image
    frontpage = Image.new('RGB', BACKGROUND_TUPLE, margin_color)
    box = tuple(numpy.add(tuple((n - o) // 2 for n, o in zip(BACKGROUND_TUPLE,LAYOUTS[layout_name]['DRAW_TUPLE'])),LAYOUTS[layout_name]['BOX_CORRECTION'])) # Correct image placement
    frontpage.paste(im, box)

    # Select title font
    title_font_name = st.sidebar.selectbox(
        label = "Select title font",
        options = files_in_folder('Fonts'),
        index = 7
    )
    # Font for first image
    title_font = ImageFont.truetype(f'Fonts/{title_font_name}', LAYOUTS[layout_name]['TITLE_SIZE'])

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

    # Check layout here because options may vary according to layout
    # If layout 2 we need to create new image to paste
    if layout_name in ['layout 2']:
        image = Image.new('RGB', (300, 45), color=margin_color)
        draw = ImageDraw.Draw(image)
        draw.text((45, 1), title_text, fill=title_color, font=title_font)
        image = image.transpose(Image.Transpose.ROTATE_90)
        frontpage.paste(image,box=(830,int(LAYOUTS[layout_name]['DRAW_TUPLE'][1]/2)-120)) # Write text on image

        # Subtitle font name
        subtitle1_font_name = st.sidebar.selectbox(
            label = "Select subtitle1 font",
            options = files_in_folder('Fonts'),
            index = 18
        )
        
        # Font for subtitle1
        subtitle1_font = ImageFont.truetype(f'Fonts/{subtitle1_font_name}', LAYOUTS[layout_name]['SUBTITLE1_SIZE'])

        #Select title text
        subtitle1_text = st.sidebar.text_input(
            label="Select subtitle1 text",
            value="www.wedreambig.com"
        )

        # Select title color 
        subtitle1_color = st.sidebar.color_picker(
            label = "Select subtitle1 color",
            value = '#DBC759' 
        )
        draw2 = ImageDraw.Draw(frontpage)
        draw2.text((728,595), subtitle1_text, fill=subtitle1_color, font=subtitle1_font,anchor="mm")

        # Subtitle font name
        subtitle2_font_name = st.sidebar.selectbox(
            label = "Select subtitle2 font",
            options = files_in_folder('Fonts'),
            index = 18
        )

        # Font for subtitle1
        subtitle2_font = ImageFont.truetype(f'Fonts/{subtitle2_font_name}', LAYOUTS[layout_name]['SUBTITLE1_SIZE'])

        #Select title text
        subtitle2_text = st.sidebar.text_input(
            label="Select postcard title",
            value="Dream Big Cambodia"
        )

        # Select title color 
        subtitle2_color = st.sidebar.color_picker(
            label = "Select title color",
            value = '#000000' 
        )
        draw2.text((135,595), subtitle2_text, fill=subtitle2_color, font=subtitle2_font,anchor="mm")

    # Select title position
    if layout_name in ['layout 1']:
        title_pos = st.sidebar.selectbox(
            label = "Select title position",
            options = LAYOUTS[layout_name]['TITLE'].keys(),
            index=0
        )
        
        # Write text on image
        image_draw = ImageDraw.Draw(frontpage)
        title_loc = LAYOUTS[layout_name]['TITLE'][title_pos]
        image_draw.text(
            title_loc, 
            title_text, 
            font=title_font, 
            fill=title_color, 
            align=LAYOUTS[layout_name]['TITLE'][title_pos], 
            anchor="mm"
        )        

        # Subtitle font name
        subtitle_font_name = st.sidebar.selectbox(
            label = "Select subtitle font",
            options = files_in_folder('Fonts'),
            index = 18
        )

        # Subtitle font
        subtitle_font = ImageFont.truetype(f'Fonts/{subtitle_font_name}', LAYOUTS[layout_name]['SUBTITLE_SIZE'])

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

        # Select subtitle position 
        title_pos = st.sidebar.selectbox(
            label = "Select subtitle position",
            options = LAYOUTS[layout_name]['SUBTITLE'].keys(),
            index=0
        )

        # Write subtitle
        subtitle_loc = LAYOUTS[layout_name]['SUBTITLE'][title_pos]
        image_draw.text(
            subtitle_loc, 
            subtitle_text, 
            font=subtitle_font, 
            fill=subtitle_color, 
            align='center', 
            anchor="mm"
        )

    # Add image filters on the sidebar
    st.sidebar.write("Filters")
    if st.sidebar.checkbox(label="invert colors"):
        frontpage_invert = ImageOps.invert(frontpage)
        frontpage = frontpage_invert
    
    if st.sidebar.checkbox(label="solarize"):
        frontpage_solar = ImageOps.solarize(frontpage)
        frontpage = frontpage_solar
    
    st.image(frontpage)
    buf = BytesIO()
    frontpage.save(buf, format="JPEG")
    byte_frontpage = buf.getvalue()
    st.download_button(
        label = "Download frontpage",
        data = byte_frontpage,
        file_name = "frontpage.png",
        mime="image/jpeg"
    )
    return frontpage

def back_page_selector():
    """
    Postcard back page selector
    """
    
    # Title 
    st.title('Back Page')

    # Description
    st.markdown(
        "- ##### Here you can visualize how the layout changes affect the postcard's backpage" 
    )

    # Title on sidebar
    st.sidebar.title("Back Page")
    
    # Upload backpage file
    file = st.sidebar.file_uploader(
        label="Upload backpage image",
        type = ['png', 'jpg','jpeg']
    )
    if file: save_in_folder('Back',file)

    # Select back page image
    backpage_name = st.sidebar.selectbox(
        label = "select backpage layout",
        options = files_in_folder('Back'),
        index = 0
    )

    backpage_img = Image.open(f'Back/{backpage_name}')
    backpage = backpage_img.resize(BACKGROUND_TUPLE)

    st.image(backpage)
    buf = BytesIO()
    backpage.save(buf, format="JPEG")
    byte_backpage = buf.getvalue()
    st.download_button(
        label = "Download backpage",
        data = byte_backpage,
        file_name = "backpage_A4.png",
        mime="image/jpeg"
    )

    return backpage

def create_final_layout(frontpage,backpage):

    front = [frontpage,frontpage]
    back = [backpage,backpage]

    horizontal_front = append_images(front, direction='horizontal')
    horizontal_back = append_images(back, direction='horizontal')

    final_front = append_images([horizontal_front,horizontal_front], direction='vertical')
    final_back = append_images([horizontal_back,horizontal_back], direction='vertical')

    buf = BytesIO()
    final_front.save(buf, format="JPEG")
    final_back.save(buf, format="JPEG")
    byte_frontpage = buf.getvalue()
    byte_backpage = buf.getvalue()

    # title
    st.title('Final layout frontpage')
    # description
    st.markdown(
        "- ##### Here you can visualize and download the frontpage layout spread by an A4 page"  
    )
    st.image(final_front)
    # download
    st.download_button(
        label = "Download frontpage A4",
        data = byte_frontpage,
        file_name = "frontpage_A4.png",
        mime="image/jpeg"
    )
    
    # title
    st.title('Final layout backpage')
    # description
    st.markdown(
        "- ##### Here you can visualize and download the backpage layout spread by an A4 page"  
    )
    st.image(final_back)
    # download
    st.download_button(
        label = "Download backpage A4",
        data = byte_backpage,
        file_name = "backpage_A4.png",
        mime="image/jpeg"
    )

    return final_front,final_back

def files_in_folder(folder:str):
    """
    Returns list of draws available inside draws folder
    """
    # List of draws 

    return next(walk(folder), (None, None, []))[2]  # [] if no file
 

def save_in_folder(folder:str, file):
    """
    Saves a file in a folder
    """
    with open(os.path.join(folder,file.name),"wb") as f:
        f.write(file.getbuffer())

def main():
    """
    Main funtion used to initalize the dashboard
    """

    # Dreambig logo
    st.image(f'Logo/dreambig_logo_A_main-1.png')
    
    # Small description of the project
    # st.markdown(
    #     "- ##### This project is an initiative created by some volunteers in order to provide to Cristina School an alternative source of revenue besides tradional donantions"
    # )
    # st.markdown(
    #     "- ##### With this webpage we intend to create a simple way for new volunteers to create new postcard layouts and customize the old ones as desired" 
    # )
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    # Video of dreambig
    # video_file = open('Video/DreamBig.mp4', 'rb')
    # video_bytes = video_file.read()
    # width = max(55, 0.01)
    # side = max((100 - width) / 2, 0.01)
    # _ , _, container = st.columns([side, width, side])
    # container.video(data=video_bytes)

    # Video of dreambig
    video_file = open('Video/DreamBig.mp4', 'rb')
    video_bytes = video_file.read()
    text_container, video_container = st.columns(2)
    text_container.markdown(
        "___________"\
    )
    text_container.text(" ")
    text_container.text(" ")
    text_container.text(" ")
    text_container.text(" ")
    text_container.markdown(
        "- ##### This project is an initiative created by some volunteers in order to provide to Cristina School an alternative source of revenue besides tradional donantions \n"\
    )
    text_container.text(" ")
    text_container.text(" ")
    text_container.text(" ")
    text_container.markdown(
        "- ##### With this webpage we intend to create a simple way for new volunteers to create new postcard layouts and customize the old ones as desired \n" \
    )
    text_container.text(" ")
    text_container.text(" ")
    text_container.text(" ")
    text_container.markdown("______")

    video_container.video(data=video_bytes)
    
    # width = max(55, 0.01)
    # side = max((100 - width) / 2, 0.01)
    # _ , _, container = st.columns([side, width, side])
    # container.video(data=video_bytes)
    

    # Cambodia country img on the sidebar
    st.sidebar.image(f'Logo/Cambodia_button_go-1.png')

    # Description of sidebar usage
    st.sidebar.title("Description")
    st.sidebar.write("On this sidebar you can edit each postcard looks by changing it's different componets")


    # create frontpage postcard img
    frontpage=postcard_creator()

    # create backpage postcard img
    backpage=back_page_selector()

    # create final layouts
    create_final_layout(
        frontpage=frontpage,
        backpage=backpage
    )

    return

main()
