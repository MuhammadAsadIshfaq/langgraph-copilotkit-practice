import React from "react";
import { Task } from "@/lib/types";

interface TaskListProps {
  tasks: Task[];
  onTaskClick: (task: Task) => void;
  onTaskDelete: (taskId: string) => void;
}

export function TaskList({ tasks, onTaskClick, onTaskDelete }: TaskListProps) {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-sm text-gray-400">
        No tasks available. Add a new task to get started.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
          onClick={() => onTaskClick(task)}
        >
          <div className="flex justify-between items-start">
            <h3 className="font-medium text-gray-900">{task.title}</h3>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onTaskDelete(task.id);
              }}
              className="text-red-500 hover:text-red-700"
            >
              Delete
            </button>
          </div>
          <p className="mt-2 text-sm text-gray-600">{task.description}</p>
          <div className="mt-4 flex items-center justify-between">
            <span className={`px-2 py-1 rounded text-xs ${
              task.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
            }`}>
              {task.status}
            </span>
            <span className={`px-2 py-1 rounded text-xs ${
              task.priority === 'high' ? 'bg-red-100 text-red-800' :
              task.priority === 'medium' ? 'bg-blue-100 text-blue-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {task.priority}
            </span>
          </div>
          {task.dueDate && (
            <div className="mt-2 text-xs text-gray-500">
              Due: {new Date(task.dueDate).toLocaleDateString()}
            </div>
          )}
        </div>
      ))}
    </div>
  );
} 