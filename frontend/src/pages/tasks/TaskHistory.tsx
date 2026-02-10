import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { fetchTasks } from '../../features/tasks/tasksSlice';
import TaskCard from '../../components/TaskCard';

const TaskHistory: React.FC = () => {
  const dispatch = useAppDispatch();
  const { tasks, loading, error } = useAppSelector((state) => state.tasks);
  const userId = useAppSelector((state) => state.auth.user?.id);

  useEffect(() => {
    dispatch(fetchTasks());
  }, [dispatch]);

  // Фильтруем завершенные задания
  const completedTasks = tasks.filter(
    (task) => task.status === 'completed' && task.executor_id === userId
  );

  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  return (
    <div className="task-history">
      <h1>История заданий</h1>
      <div className="tasks-list">
        {completedTasks.length === 0 ? (
          <p>У вас нет завершенных заданий</p>
        ) : (
          completedTasks.map((task) => (
            <div key={task.id} className="completed-task">
              <TaskCard task={task} />
              <div className="completion-info">
                <span className="status-badge">Завершено</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TaskHistory;
