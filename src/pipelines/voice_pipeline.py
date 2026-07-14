# from speechbrain.inference.speaker import EncoderClassifier
# import numpy as np
# import io
# import librosa
# import streamlit as st
# import tempfile
# import os
# import soundfile as sf

# @st.cache_resource
# def load_voice_encoder():
#     return EncoderClassifier.from_hparams(
#         source="speechbrain/spkrec-ecapa-voxceleb"
#     )


# def get_voice_embedding(audio_bytes):
#     try:
#         classifier = load_voice_encoder()

#         # Temporary file create
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
#             f.write(audio_bytes)
#             temp_path = f.name

#         # Generate embedding
#         embedding = classifier.encode_file(temp_path)

#         # Delete temp file
#         os.remove(temp_path)

#         return embedding.squeeze().cpu().numpy().tolist()

#     except Exception as e:
#         st.error(f"Voice Recognition Error: {e}")
#         return None
    
# def idetify_speaker(new_embedding, candidates_dict, threshold= 0.65):
#     if new_embedding in None or not candidates_dict:
#         return None, 0.0
#     best_sid = None
#     best_score = -1.0

#     for sid, storded_embedding in candidates_dict.items():
#         if storded_embedding:
#             similarity = np.dot(new_embedding, storded_embedding)
#             if similarity>best_score:
#                 best_score = similarity
#                 best_sid = sid

#     if best_score>=threshold:
#         return best_sid, best_score
#     return None, best_score



# def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
#     try:
#         classifier = load_voice_encoder()

#         audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
#         segments = librosa.effects.split(audio, top_db=30)

#         identified_results = {}

#         for start, end in segments:

#             if (end - start) < sr * 0.5:
#                 continue

#             segment_audio = audio[start:end]

#             with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
#                 sf.write(f.name, segment_audio, sr)

#                 embedding = classifier.encode_file(f.name)

#             os.remove(f.name)

#             embedding = embedding.squeeze().cpu().numpy()

#             sid, score = idetify_speaker(
#                 embedding,
#                 candidates_dict,
#                 threshold
#             )

#             if sid:
#                 if sid not in identified_results or score > identified_results[sid]:
#                     identified_results[sid] = score

#         return identified_results

#     except Exception as e:
#         st.error(f"Bulk process error: {e}")
#         return {}