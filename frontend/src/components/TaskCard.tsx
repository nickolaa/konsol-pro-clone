import React from 'react';
import { Task } from '../features/tasks/tasksSlice';
import { Link } from 'react-router-dom';

interface TaskCardProps {
  task: Task;
}

const TaskCard: React.FC<TaskCardProps> = ({ task }) => {
  return (
    <div className="task-card">
      <Link to={`/tasks/${task.id}`}>
        <h3>{task.title}</h3>
      </Link>
      <p className="task-description">{task.description}</p>
      <div className="task-meta">
        <span className="task-budget">Бюджет: {task.budget} ₽</span>
        <span className="task-category">Категория: {task.category}</span>
        <span className="task-deadline">
          Дедлайн: {new Date(task.deadline).toLocaleDateString('ru-RU')}
        </span>
      </div>
      <div className="task-company">
        <strong>Компания:</strong> {task.company_name || 'Не указана'}
      </div>
    </div>
  );
};

export default TaskCard;
