import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  posts: [],
  post: null,
  newPost: null,
  modifiedPost: null,
};

const postsSlice = createSlice({
  name: "posts",
  initialState,
  reducers: {
    setPost: (state, action) => {
      state.post = action.payload;
    },
    modifyPost: (state, action) => {
      state.modifiedPost = action.payload;
    },
    likePost: (state, action) => {
      state.modifiedPost = action.payload;
    },
    unlikePost: (state, action) => {
      state.modifiedPost = action.payload;
    },
    setPosts: (state, action) => {
      state.posts = action.payload;
    },
    setNewPost: (state, action) => {
      state.newPost = action.payload;
    },
  },
});

export const { setPost, modifyPost, likePost, unlikePost, setPosts, setNewPost } = postsSlice.actions;

export default postsSlice.reducer;