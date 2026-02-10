import React, { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../app/hooks';
import { fetchTasks } from '../../features/tasks/tasksSlice';
import TaskCard from '../../components/TaskCard';

const TaskFeed: React.FC = () => {
  const dispatch = useAppDispatch();
  const { tasks, loading, error } = useAppSelector((state) => state.tasks);
  const [filters, setFilters] = useState({
    search: '',
    category: '',
    minBudget: '',
    maxBudget: '',
  });

  useEffect(() => {
    dispatch(fetchTasks());
  }, [dispatch]);

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const filteredTasks = tasks.filter((task) => {
    const matchesSearch = task.title.toLowerCase().includes(filters.search.toLowerCase());
    const matchesCategory = filters.category === '' || task.category === filters.category;
    const matchesBudget =
      (filters.minBudget === '' || task.budget >= Number(filters.minBudget)) &&
      (filters.maxBudget === '' || task.budget <= Number(filters.maxBudget));
    return matchesSearch && matchesCategory && matchesBudget && task.status === 'published';
  });

  if (loading) return <div className="loading">Загрузка заданий...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  return (
    <div className="task-feed">
      <h1>Лента заданий</h1>
      
      <div className="filters">
        <input
          type="text"
          name="search"
          placeholder="Поиск по названию"
          value={filters.search}
          onChange={handleFilterChange}
        />
        <select name="category" value={filters.category} onChange={handleFilterChange}>
          <option value="">Все категории</option>
          <option value="development">Разработка</option>
          <option value="design">Дизайн</option>
          <option value="marketing">Маркетинг</option>
          <option value="writing">Копирайтинг</option>
        </select>
        <input
          type="number"
          name="minBudget"
          placeholder="Мин. бюджет"
          value={filters.minBudget}
          onChange={handleFilterChange}
        />
        <input
          type="number"
          name="maxBudget"
          placeholder="Макс. бюджет"
          value={filters.maxBudget}
          onChange={handleFilterChange}
        />
      </div>

      <div className="tasks-list">
        {filteredTasks.length === 0 ? (
          <p>Нет доступных заданий</p>
        ) : (
          filteredTasks.map((task) => <TaskCard key={task.id} task={task} />)
        )}
      </div>
    </div>
  );
};

export default TaskFeed;
