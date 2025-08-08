import { useAuth } from '../contexts/AuthContext';

const Login = () => {
  const { user, login, logout } = useAuth();

  return (
    <>
    <div className="place-items-center my-100">
      {!user ? (
        <button onClick={login}>Log in with Google</button>
      ) : (
        <button onClick={logout}>Log out</button>
      )}
    </div>
    </>
  );
}

export default Login;