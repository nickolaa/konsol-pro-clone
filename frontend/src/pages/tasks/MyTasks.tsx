import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { fetchTasks } from '../../features/tasks/tasksSlice';
import TaskCard from '../../components/TaskCard';

const MyTasks: React.FC = () => {
  const dispatch = useAppDispatch();
  const { tasks, loading, error } = useAppSelector((state) => state.tasks);
  const userId = useAppSelector((state) => state.auth.user?.id);

  useEffect(() => {
    dispatch(fetchTasks());
  }, [dispatch]);

  // Фильтруем задания, на которые откликнулся пользователь или которые выполняет
  const myTasks = tasks.filter(
    (task) => task.status === 'in_progress' && task.executor_id === userId
  );

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  return (
    <div className="my-tasks">
      <h1>Мои активные задания</h1>
      <div className="tasks-list">
        {myTasks.length === 0 ? (
          <p>У вас нет активных заданий</p>
        ) : (
          myTasks.map((task) => <TaskCard key={task.id} task={task} />)
        )}
      </div>
    </div>
  );
};

export default MyTasks;
