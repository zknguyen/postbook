import { useAuth } from '../contexts/AuthContext';
import NewPostForm from '../components/posts/NewPostForm';
import FollowUserForm from '../components/follows/FollowUserForm';
import Feed from '../components/feed/Feed';

const Home = () => {
  const { user } = useAuth();

  return (
    <>
      <div className="grid grid-cols-3 w-full justify-self-center my-4">
        <h2 className="col-span-3">Welcome back, {user.Username}</h2>
        <div className="col-start-2">
          <NewPostForm />
          <Feed />
        </div>
        <FollowUserForm />
      </div>
    </>
  )
}

export default Home;