import streamlit as st
import json
import os

def main():
    # Define a state variable to track if the process button has been clicked
    process_clicked = st.session_state.get('process_clicked', False)

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Our Favorites")
    available_podcast_info = create_dict_from_json_files('.')
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")

    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("**Note**: Podcast processing can take up to 6 mins, please bear with us.")

    if process_button:
        st.session_state.process_clicked = True

        # Call the function to process the URLs and retrieve podcast guest information
        podcast_info = process_podcast_info(url)

        # Code to render the content after processing
        render_podcast_content(podcast_info)

    elif selected_podcast and not process_clicked:
        st.session_state.process_clicked = False

        podcast_info = available_podcast_info[selected_podcast]
        render_podcast_content(podcast_info)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}
    json_files.reverse()
    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    # Placeholder function for processing podcasts; replace with actual implementation
    # Example data returned
    return {
        'podcast_details': {'podcast_title': 'Example Podcast', 'episode_title': 'Episode 1', 'episode_image': 'image_url'},
        'podcast_summary': 'This is an example summary',
        'podcast_guest': {'name': 'Guest Name', 'summary': 'Guest summary'},
        'podcast_highlights': 'Key moments here\nAnother key moment',
        'podcast_dalle': {'image_url': 'background_image_url'}
    }

def render_podcast_content(podcast_info):
    background_image_url = podcast_info.get('podcast_dalle', {}).get('image_url', 'default_image_url')

    header_html = f"""
    <div id="dallepic" style="background-image: url('{background_image_url}'); background-size: cover; background-repeat: no-repeat; padding: 20px; text-align: center; height: 100%; width: 100%; display: flex; align-items: center; justify-content: center;">
        <span style="color: white; font-size: 60px; font-weight: bold; text-shadow: 2px 2px 4px #000000;">
            Benny's Podcasts
        </span>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    st.markdown("Background by DALL·E 2")

    # Right section - Newsletter content
    st.header(podcast_info['podcast_details']['episode_title'])

    # Display the podcast title
    st.subheader(podcast_info['podcast_details']['podcast_title'])
    st.write()

    # Display the podcast summary and the cover image in a side-by-side layout
    col1, col2 = st.columns([7, 3])

    with col1:
        # Display the podcast episode summary
        st.subheader("Podcast Episode Summary")
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

if __name__ == '__main__':
    main()
