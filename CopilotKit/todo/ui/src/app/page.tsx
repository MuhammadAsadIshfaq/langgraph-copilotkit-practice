'use client';

import { useState } from 'react';
import { CopilotKit } from '@copilotkit/react-core';
import { CopilotSidebar } from '@copilotkit/react-ui';
import TodoList from '../components/TodoList';
import AddTodo from '../components/AddTodo';

export default function Home() {
  const [todos, setTodos] = useState<Array<{ id: number; text: string; completed: boolean }>>([]);

  const addTodo = (text: string) => {
    setTodos([...todos, { id: Date.now(), text, completed: false }]);
  };

  const toggleTodo = (id: number) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  const deleteTodo = (id: number) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <CopilotKit>
      <main className="min-h-screen bg-gray-100 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
            AI-Powered Todo App
          </h1>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <AddTodo onAdd={addTodo} />
            <TodoList
              todos={todos}
              onToggle={toggleTodo}
              onDelete={deleteTodo}
            />
          </div>
        </div>
        <CopilotSidebar
          defaultOpen={true}
          className="w-96"
        />
      </main>
    </CopilotKit>
  );
} 