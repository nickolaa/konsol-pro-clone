import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from './app/store';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import TaskFeed from './pages/tasks/TaskFeed';
import MyTasks from './pages/tasks/MyTasks';
import TaskHistory from './pages/tasks/TaskHistory';

// Placeholder components
const Dashboard = () => <div><h1>Панель управления</h1></div>;
const Home = () => <div><h1>Главная страница</h1></div>;

// Protected route wrapper
interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
            <Route path="/tasks" element={<TaskFeed />} />
      <Route
        path="/my-tasks"
        element={
          <ProtectedRoute>
            <MyTasks />
          </ProtectedRoute>
        }
      />
      <Route
        path="/task-history"
        element={
          <ProtectedRoute>
            <TaskHistory />
          </ProtectedRoute>
        }
      />
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } 
      />
    </Routes>
  );
};

export default AppRoutes;
