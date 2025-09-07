import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const CreateUser = () => {
  const navigate = useNavigate();
  const { token, user, setUser } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData(e.target);
      const firebaseUid = user.uid;
      const body = {
        'Username': formData.get('username'),
        'FirstName': formData.get('first_name'),
        'LastName': formData.get('last_name'),
        'Email': formData.get('email'),
        'FirebaseUID': firebaseUid,
      };

      const response = await fetch(`${import.meta.env.VITE_API_SERVER_URL}/v1/users`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      if (!response.ok) {
        throw new Error('Failed to create user');
      }

      const data = await response.json();
      const userId = data.UserID;

      console.log(`User created with ID: ${userId}`);
      const response2 = await fetch(`${import.meta.env.VITE_API_SERVER_URL}/v1/users/${userId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      if (!response2.ok) {
        throw new Error('Failed to retrieve user');
      }

      const userData = await response2.json();
      setUser(userData);
      navigate('/');
    } catch (error) {
      console.error('Create user failed: ', error);
    }
  };

  // TODO: set default colors
  // TODO: fix css formatting
  return (
    <div className="my-80">
      <form
        className="
          [&_input]:text-[#D3D3D3] [&_input]:bg-neutral-700
          [&_input]:rounded-lg [&_input]:border-none
          [&_input]:px-2 [&_input]:py-1
          [&_input]:my-1
        "
        name="create-user-form"
        onSubmit={handleSubmit}
      >
        <input type="text" name="username" placeholder="Username" required /><br />
        <input type="text" name="first_name" placeholder="First Name" required /><br />
        <input type="text" name="last_name" placeholder="Last Name" required /><br />
        <input type="text" name="email" placeholder="Email" required /><br />
        <button type="submit">Submit</button><br />
      </form>
    </div>
  )
}

export default CreateUser;