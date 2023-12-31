##this works and shows both in same but stacked on top of each other

import streamlit as st
import modal
import json
import os

def main():
    
    
    background_image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-xAcx2hRn6fPSUBTjqXxrTV7S/user-2dDRPrUmKcI75xLvAOsTk12c/img-xZ0bNWhE6462QRCxS34k1UIC.png?st=2023-08-17T21%3A05%3A42Z&se=2023-08-17T23%3A05%3A42Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-08-17T17%3A52%3A03Z&ske=2023-08-18T17%3A52%3A03Z&sks=b&skv=2021-08-06&sig=FK4tMXX1Jp2kq338QMCnVkQQhs7JayBT1jhNGh8Ea2A%3D"
    
    # Create a custom header with the background image
    header_html = f"""
    <div id="dallepic" style="background-image: url('{background_image_url}'); background-size: cover; background-repeat: no-repeat; padding: 20px; text-align: center; height: 300px; width: 100%; display: flex; align-items: center; justify-content: center;">
        <span style="color: white; font-size: 60px; font-weight: bold; text-shadow: 2px 2px 4px #000000;">
            Benny's Podcasts
        </span>
    </div>

    """
    
    # Use the `st.markdown` method to render the HTML
    #st.markdown(header_html, unsafe_allow_html=True)

    


    ######1
     

    ######2
    
    # st.title("Benny's Podcasts")

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Our Favorites")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    if selected_podcast:

        podcast_info = available_podcast_info[selected_podcast]
        background_image_url = podcast_info.get('podcast_dalle', {}).get('image_url', 'default_image_url')

        


        # Create a custom header with the background image
        header_html = f"""
        <div id="dallepic"style="background-image: url('{background_image_url}'); background-size: cover; background-repeat: no-repeat; padding: 20px; text-align: center; height: 500px; width: 100%; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 60px; font-weight: bold; text-shadow: 2px 2px 4px #000000;">
                Benny's Podcasts
            </span>
        </div>
        """
    
        # Use the `st.markdown` method to render the HTML
        st.markdown(header_html, unsafe_allow_html=True)
        st.markdown("Background by DALL·E 2")
        # Right section - Newsletter content
        st.header(podcast_info['podcast_details']['episode_title'])

        # Display the podcast title
        st.subheader(selected_podcast)
        st.write("")

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.subheader("Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption=selected_podcast, width=300, use_column_width=True)

        # Display the podcast guest and their details in a side-by-side layout
        col3, col4 = st.columns([3, 7])

        with col3:
            st.subheader("Podcast Guest")
            st.write(podcast_info['podcast_guest']['name'])

        with col4:
            st.subheader("Podcast Guest Details")
            st.write(podcast_info["podcast_guest"]['summary'])

        # Display the five key moments
        st.subheader("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")

    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("**Note**: Podcast processing can take up to 6 mins, please bear with us.")

    if process_button:

        # Call the function to process the URLs and retrieve podcast guest information
        podcast_info = process_podcast_info(url)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        background_image_url = podcast_info.get('podcast_dalle', {}).get('image_url', 'default_image_url')

        


        # Create a custom header with the background image
        header_html = f"""
        <div id="dallepic"style="background-image: url('{background_image_url}'); background-size: cover; background-repeat: no-repeat; padding: 20px; text-align: center; height: 500px; width: 100%; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 60px; font-weight: bold; text-shadow: 2px 2px 4px #000000;">
                Benny's Podcasts
            </span>
        </div>
        """
    
        # Use the `st.markdown` method to render the HTML
        st.markdown(header_html, unsafe_allow_html=True)
        st.markdown("Background by DALL·E 2")
        # Right section - Newsletter content
        st.header(podcast_info['podcast_details']['episode_title'])
        #podcast_title
        # Display the podcast title
        st.subheader(podcast_info['podcast_details']['podcast_title'])
        st.write()

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.subheader("Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption=podcast_info['podcast_details']['podcast_title'], width=300, use_column_width=True)

        # Display the podcast guest and their details in a side-by-side layout
        col3, col4 = st.columns([3, 7])

        with col3:
            st.subheader("Podcast Guest")
            st.write(podcast_info['podcast_guest']['name'])

        with col4:
            st.subheader("Podcast Guest Details")
            st.write(podcast_info["podcast_guest"]['summary'])

        # Display the five key moments
        st.subheader("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}
    json_files.reverse()
    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            # Process the file data as needed
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()
