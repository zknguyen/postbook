// Component to follow a user
import { useAuth } from '../../contexts/AuthContext';

const FollowUserForm = () => {
  const { user, headers } = useAuth();

  const handleFormSubmitted = async (e) => {
    e.preventDefault();
    try {
      // Look for user
      const formData = new FormData(e.target);

      const response = await fetch(
        `${import.meta.env.VITE_API_SERVER_URL}/v1/users/?limit=1&offset=0&Username=${formData.get('username')}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );
      const data = await response.json();
      if (data.hasOwnProperty('detail')) {
        // TODO: Find a better way to handle this
        console.log('No user found.');
        return;
      }

      // Create follow relationship
      const body = {
        FollowerID: user.UserID,
        FolloweeID: data[0].UserID,
      };

      const response2 = await fetch(`${import.meta.env.VITE_API_SERVER_URL}/v1/follows`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      const data2 = await response2.json();
      if (data2.hasOwnProperty('FollowID')) {
        console.log('Follow successful!');
        // TODO: Update feed
      } else {
        // TODO: Find a better way to handle this
        console.log('Could not follow user.');
      }
    } catch (error) {
      console.error('Failed to follow user.');
    }
  };

  return (
    <form onSubmit={handleFormSubmitted}>
      <h3>Follow a User:</h3>
      <input
        className="
          text-[#D3D3D3] bg-neutral-700
          rounded-lg border-none
          w-4/5
          px-2 py-1
          my-1
        "
        type="text"
        name="username"
        placeholder="Username"
        required
      />
      <br />
      <button type="submit">Submit</button>
      <br />
    </form>
  );
};

export default FollowUserForm;