import streamlit as st
import streamlit.components.v1 as components
import json

from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem
from twelvelabs.tasks import TasksRetrieveResponse



st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #000000; /* black background */
    color: #FFFFFF; /* white text */
    font-family: 'Century', serif;
}

/* Buttons */
.stForm .stButton button {
    background-color: #643173; /* vivid purple */
    color: #FFFFFF; /* white text for contrast */
    border-radius: 12px;
    padding: 0.6em 1.2em;
    font-weight: bold;
    border: none;
    font-size: 1.4rem;
}

/* Optional: Hover effect */
.stForm .stButton button:hover {
    background-color: #532463; /* slightly darker shade on hover */
}

/* Input box */
.stTextInput > div > div > input {
    background-color: #86A59C; /* gray-green input field */
    color: #1F271B; /* green-black text for readability */
    border: 2px solid #89CE94; /* bright green border for visibility */
    border-radius: 8px;
    padding: 0.5em;
    font-size: 1.4rem;
}

/* Success message tweaks */
.stAlert {
    background-color: #228B22; /* strong green background */
    color: #FFFFFF; /* white text */
    border-radius: 8px;
    font-weight: bold;
    font-size: 1.2rem;
}
</style>
""", unsafe_allow_html=True)




# =========================
# TITLE
# =========================
st.markdown('<h1 style="color:#1C77C3; text-align:center;">Custom Workout Clip Finder</h1>', unsafe_allow_html=True)



# =========================
# DROPDOWNS FOR WORKOUT SELECTION
# =========================
workout_options = ['None', 'core', 'glutes', 'weights', 'bodyweight only', 'pregnancy friendly']
avoid_options = ['None', 'standing', 'applying pressure to wrists', 'jumping']

# Define the workout and avoid options
workout_options = ['None', 'core', 'glutes', 'weights', 'bodyweight only', 'pregnancy friendly']
avoid_options = ['None', 'standing', 'applying pressure to wrists', 'jumping']


st.markdown("**Choose what you'd like your workout to have and what you'd like to avoid, and we will select the perfect workout video clips to match your specifications!**")

# Create the form
with st.form(key='workout_form'):
    # Involve section
    st.markdown("**I want my workout to involve:**")
    cols = st.columns(3)
    involve1 = cols[0].selectbox("", workout_options, key="involve1")
    involve2 = cols[1].selectbox("", workout_options, key="involve2")
    involve3 = cols[2].selectbox("", workout_options, key="involve3")

    # Avoid section
    st.markdown("**And avoid:**")
    cols_avoid = st.columns(2)
    avoid1 = cols_avoid[0].selectbox("", avoid_options, key="avoid1")
    avoid2 = cols_avoid[1].selectbox("", avoid_options, key="avoid2")

    # Create a submit button
    submit_button = st.form_submit_button(label='Submit')

    # Handle form submission
    if submit_button:
        selected_involve = [x for x in [involve1, involve2, involve3] if x != "None"]
        selected_avoid = [x for x in [avoid1, avoid2] if x != "None"]

        # Check if all fields are filled
        if len(selected_involve) == 0 or len(selected_avoid) == 0:
            st.warning("Please select at least one option in each category (Involve and Avoid).")
        else:
            # Display the user's selections
            st.write("You want your workout to involve:", selected_involve)
            st.write("You want to avoid:", selected_avoid)




involve = ' '.join(s for s in [involve1, involve2, involve3] if s)
avoid = ' '.join(s for s in [avoid1, avoid2] if s)

client = TwelveLabs(api_key="tlk_0R4RVJ32PB8GQK2AS38HS061C93Q")
client_index_id = "68cf29735705aa622334a87f"


if submit_button:
    query = "Find me the top three clips in all the videos that focus on " + involve + " and avoid " + avoid

    st.write("Your Exercises...")


    ## First API call 
    search_pager = client.search.query(
        index_id=client_index_id, query_text=query, search_options=["visual", "audio"],)


    vid0_id = search_pager.items[0].video_id
    vid0_start_time = search_pager.items[0].start

    vid1_id = search_pager.items[1].video_id
    vid1_start_time = search_pager.items[1].start

    vid2_id = search_pager.items[2].video_id
    vid2_start_time = search_pager.items[2].start



    # Second API call 
    vid0_url_info = client.indexes.videos.retrieve(index_id=client_index_id, video_id=vid0_id)
    vid0_url = json.loads(vid0_url_info.json())['hls']['video_url']

    # Third API call 
    vid1_url_info = client.indexes.videos.retrieve(index_id=client_index_id, video_id=vid1_id)
    vid1_url = json.loads(vid1_url_info.json())['hls']['video_url']

    # Fourth API call 
    vid2_url_info = client.indexes.videos.retrieve(index_id=client_index_id, video_id=vid2_id)
    vid2_url = json.loads(vid2_url_info.json())['hls']['video_url']

    components.html(
        f"""
        <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            </head>
            <body>
                <video id="video" width="800" controls>
                    <source src="{vid0_url}" type="application/x-mpegURL">
                    Your browser does not support the video tag.
                </video>

                <script>
                    var video = document.getElementById('video');

                    // Check if HLS.js is supported for HLS playback
                    if (Hls.isSupported()) {{
                        var hls = new Hls();
                        hls.loadSource("{vid0_url}");
                        hls.attachMedia(video);
                    }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                        video.src = "{vid0_url}";
                    }}

                    // Set video start time when the play button is clicked
                    video.addEventListener('play', function() {{
                        video.currentTime = {vid0_start_time};  // Automatically jump to the defined start time
                    }});
                </script>
            </body>
        </html>
        """,
        height=500,
    )



    components.html(
        f"""
        <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            </head>
            <body>
                <video id="video" width="800" controls>
                    <source src="{vid1_url}" type="application/x-mpegURL">
                    Your browser does not support the video tag.
                </video>

                <script>
                    var video = document.getElementById('video');

                    // Check if HLS.js is supported for HLS playback
                    if (Hls.isSupported()) {{
                        var hls = new Hls();
                        hls.loadSource("{vid1_url}");
                        hls.attachMedia(video);
                    }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                        video.src = "{vid1_url}";
                    }}

                    // Set video start time when the play button is clicked
                    video.addEventListener('play', function() {{
                        video.currentTime = {vid1_start_time};  // Automatically jump to the defined start time
                    }});
                </script>
            </body>
        </html>
        """,
        height=500,
    )



    components.html(
        f"""
        <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            </head>
            <body>
                <video id="video" width="800" controls>
                    <source src="{vid2_url}" type="application/x-mpegURL">
                    Your browser does not support the video tag.
                </video>

                <script>
                    var video = document.getElementById('video');

                    // Check if HLS.js is supported for HLS playback
                    if (Hls.isSupported()) {{
                        var hls = new Hls();
                        hls.loadSource("{vid2_url}");
                        hls.attachMedia(video);
                    }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                        video.src = "{vid2_url}";
                    }}

                    // Set video start time when the play button is clicked
                    video.addEventListener('play', function() {{
                        video.currentTime = {vid2_start_time};  // Automatically jump to the defined start time
                    }});
                </script>
            </body>
        </html>
        """,
        height=500,
    )




