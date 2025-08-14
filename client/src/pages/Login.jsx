import { useAuth } from '../contexts/AuthContext';

const Login = () => {
  const { login, loading } = useAuth();

  if (loading) return <div>Loading...</div>;

  return (
    <div className="h-screen justify-center items-center flex">
      <button onClick={login}>Sign in with Google</button>
    </div>
  );
};

export default Login;