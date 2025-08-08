import { useAuth } from '../../contexts/AuthContext';
import { useDispatch } from 'react-redux';
import { setNewPost } from '../../redux/state/postsSlice.jsx';

const NewPostForm = () => {
  const { user, headers } = useAuth();
  const dispatch = useDispatch();

  const handleFormSubmitted = async (e) => {
    e.preventDefault();
    try {
      // TODO: Move this logic elsewhere
      const formData = new FormData(e.target);
      const postBody = {
        'UserID': user.UserID,
        'TextContent': formData.get('text-content'),
      };

      const response = await fetch(`${import.meta.env.VITE_API_SERVER_URL}/v1/posts`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(postBody),
      });
      if (!response.ok) {
        throw new Error('Failed to create post');
      }

      const data = await response.json();

      // Push post to followers' feeds
      // TODO: Move this logic elsewhere
      const feedPostBody = {
        'PostID': data.PostID,
      }
      const response2 = await fetch(`${import.meta.env.VITE_API_SERVER_URL}/v1/feeds/posts/${user.UserID}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feedPostBody),
      });
      if (response2.ok) {
        // Refresh current feed view with new post
        dispatch(setNewPost(data));
      } else {
        console.warn('Could not update followers\' feeds.');
      }
      e.target.reset();
    } catch (error) {
      console.error(error);
    }
  }
  return (
    <form className="bg-neutral-800 rounded-lg p-2 my-5" onSubmit={handleFormSubmitted}>
      <h3>Make a Post:</h3>
      <input
        className="
          text-[#D3D3D3] bg-neutral-700
          rounded-lg border-none
          w-full
          px-2 py-1
          my-1
          focus:outline-none
        "
        type="text" name="text-content" placeholder="Say something..." required
      />
      <br />
      <button type="submit">Post</button><br />
    </form>
  )
}

export default NewPostForm;