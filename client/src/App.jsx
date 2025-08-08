import { Route, Routes, useLocation } from 'react-router-dom';

import ProtectedRoutes from './utils/ProtectedRoutes';

import CreateUser from './pages/CreateUser';
import Home from './pages/Home';
import Login from './pages/Login';
import Post from './pages/Post';
import UserProfile from './pages/UserProfile';
import Navbar from './components/navbar/Navbar';

import './App.css';

function App() {
  const location = useLocation();
  const hideNavbar = location.pathname === '/login' || location.pathname === '/create-user';

  return (
    <>
      {!hideNavbar && <Navbar />}
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoutes />}>
          <Route path="/" element={<Home />} />
          <Route path="/create-user" element={<CreateUser />} />
          <Route path="/post/:postId" element={<Post />} />
          <Route path="/user/:userId" element={<UserProfile />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
