import { configureStore } from '@reduxjs/toolkit';
import postsReducer from './state/postsSlice.jsx';


const store = configureStore({
  reducer: {
    posts: postsReducer,
  },
});

export default store;