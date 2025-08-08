import { useNavigate } from 'react-router-dom';

import { useAuth } from '../../contexts/AuthContext';
import viteLogo from '../../../public/vite.svg';

const Navbar = () => {
  const { logout } = useAuth();

  const navigate = useNavigate();

  const LogoutButton = () => {
    return (
      <button onClick={logout}>Log out</button>
    )
  };

  const handleLogoClick = () => {
    navigate('/');
  };

  return (
    <div className="bg-neutral-800 w-full px-4 py-2 inline-flex justify-between">
        <img src={viteLogo} className="logo hover:cursor-pointer" alt="Vite logo" onClick={handleLogoClick} />
      <LogoutButton />
    </div>
  );
}

export default Navbar;