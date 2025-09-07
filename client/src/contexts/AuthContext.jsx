import { createContext, useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth, provider } from './firebase';
import { onAuthStateChanged, signInWithPopup, signOut } from 'firebase/auth';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(true);
  
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
  };

  const login = async () => {
    try {
      const userCredential = await signInWithPopup(auth, provider);
      const token = await userCredential.user.getIdToken();
      setToken(token);
      // Verify user
      const response = await fetch(`${import.meta.env.VITE_API_SERVER_URL}/v1/users/by-firebase-id/${userCredential.user.uid}`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`
        },
      });
      if (!response.ok) {
        throw new Error('Could not verify user');
      }
      
      const data = await response.json();

      // Navigate to createUser page if there isn't a user registered with the login email
      if (data) {
        setUser(data);
        navigate('/');
      } else {
        navigate('/create-user');
      }
    } catch (error) {
      console.error('Login failed: ', error);
    }
  };

  const logout = async () => {
    await signOut(auth);
    setUser(null);
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, token, login, logout, loading, headers }}>
      {!loading && children}
    </AuthContext.Provider>
  );
}