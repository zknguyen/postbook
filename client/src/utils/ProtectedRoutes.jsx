import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext.jsx';

const ProtectedRoutes = () => {
    const { user, loading } = useAuth();

    if (loading) {
        return <div>Loading...</div>; // TODO: Replace with loading spinner/bar
    }

    return user ? <Outlet /> : <Navigate to="/login" />;
}

export default ProtectedRoutes;