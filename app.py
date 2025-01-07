import os
import io
import streamlit as st
from streamlit_image_select import image_select
import torch
from wav2lip import inference
from wav2lip.models import Wav2Lip
import gdown
device = "cpu"


# @st.cache_data is used to only load the model once
# @st.cache_data
@st.cache_resource
def load_model(path):
    st.write("Please wait for the model to be loaded or it will cause an error")
    wav2lip_checkpoints_url = "https://drive.google.com/drive/folders/1Sy5SHRmI3zgg2RJaOttNsN3iJS9VVkbg?usp=sharing"
    if not os.path.exists(path):
        gdown.download_folder(wav2lip_checkpoints_url, quiet=True, use_cookies=False)
    st.write("Please wait")
    model = Wav2Lip()
    print("Load checkpoint from: {}".format(path))
    checkpoint = torch.load(path, map_location=lambda storage, loc: storage)
    s = checkpoint["state_dict"]
    new_s = {}
    for k, v in s.items():
        new_s[k.replace("module.", "")] = v
    model.load_state_dict(new_s)
    model = model.to(device)
    st.write("model is loaded!")
    return model.eval()


@st.cache_resource
def load_avatar_videos_for_slow_animation(path):
    avatar_videos_url = "https://drive.google.com/drive/folders/1h9pkU5wenrS2vmKqXBfFmrg-1hYw5s4q?usp=sharing"
    if not os.path.exists(path):
        gdown.download_folder(avatar_videos_url, quiet=True, use_cookies=False)


image_video_map = {
    "avatars_images/avatar1.jpg": "avatars_videos/avatar1.mp4",
    "avatars_images/avatar2.jpg": "avatars_videos/avatar2.mp4"
}


def streamlit_look():
    """
    Modest front-end code:)
    """
    data = {}
    st.title("Welcome to AI Lip Sync :)")
    st.write("Please choose your avatar from the following options:")
    avatar_img = image_select(
        "",
        [
            "avatars_images/avatar1.jpg",
            "avatars_images/avatar2.jpg"
        ],
    )
    data["imge_path"] = avatar_img
    return data


def main():
    data = streamlit_look()
    st.write(
        "With fast animation only the lips of the avatar will move, and it will take probably less than a minute for a record of about 30 seconds, but with fast animation choise, the full face of the avatar will move and it will take about 30 minute for a record of about 30 seconds to get ready."
    )
    model = load_model("wav2lip_checkpoints/wav2lip_gan.pth")
    fast_animate = st.button("fast animate")
    slower_animate = st.button("slower animate")
    if fast_animate:
        inference.main(data["imge_path"], "record.wav", model)
        if os.path.exists("wav2lip/results/result_voice.mp4"):
            st.video("wav2lip/results/result_voice.mp4")
    if slower_animate:
        load_avatar_videos_for_slow_animation("avatars_videos")
        inference.main(image_video_map[data["imge_path"]], "record.wav", model)
        if os.path.exists("wav2lip/results/result_voice.mp4"):
            st.video("wav2lip/results/result_voice.mp4")


if __name__ == "__main__":
    main()
