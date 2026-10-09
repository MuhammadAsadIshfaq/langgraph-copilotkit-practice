"use client";

import { useState, useEffect } from "react";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import axios from "axios";

interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: string;
  due_date?: string;
}

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [newTodo, setNewTodo] = useState({
    title: "",
    description: "",
    priority: "medium",
    due_date: "",
  });

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await axios.get("http://localhost:8000/todos");
      setTodos(response.data.todos);
    } catch (error) {
      console.error("Error fetching todos:", error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/chat", {
        content: message,
      });
      setResponse(response.data.response);
      setMessage("");
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/todos", newTodo);
      setNewTodo({
        title: "",
        description: "",
        priority: "medium",
        due_date: "",
      });
      fetchTodos();
    } catch (error) {
      console.error("Error creating todo:", error);
    }
  };

  const handleToggleComplete = async (todoId: string, completed: boolean) => {
    try {
      await axios.put(`http://localhost:8000/todos/${todoId}`, {
        completed: !completed,
      });
      fetchTodos();
    } catch (error) {
      console.error("Error updating todo:", error);
    }
  };

  const handleDeleteTodo = async (todoId: string) => {
    try {
      await axios.delete(`http://localhost:8000/todos/${todoId}`);
      fetchTodos();
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  };

  return (
    <CopilotKit
      apiKey={process.env.NEXT_PUBLIC_COPILOT_API_KEY}
      baseURL="http://localhost:8000"
    >
      <div className="min-h-screen bg-gray-100">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-8">AI Todo Assistant</h1>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Chat Interface */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-semibold mb-4">Chat with AI Assistant</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  className="w-full p-2 border rounded"
                  rows={4}
                  placeholder="Ask about your todos or get suggestions..."
                />
                <button
                  type="submit"
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Send
                </button>
              </form>
              {response && (
                <div className="mt-4 p-4 bg-gray-50 rounded">
                  <p className="whitespace-pre-wrap">{response}</p>
                </div>
              )}
            </div>

            {/* Create Todo Form */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-semibold mb-4">Create New Todo</h2>
              <form onSubmit={handleCreateTodo} className="space-y-4">
                <input
                  type="text"
                  value={newTodo.title}
                  onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
                  className="w-full p-2 border rounded"
                  placeholder="Title"
                  required
                />
                <textarea
                  value={newTodo.description}
                  onChange={(e) => setNewTodo({ ...newTodo, description: e.target.value })}
                  className="w-full p-2 border rounded"
                  placeholder="Description"
                  rows={3}
                />
                <select
                  value={newTodo.priority}
                  onChange={(e) => setNewTodo({ ...newTodo, priority: e.target.value })}
                  className="w-full p-2 border rounded"
                >
                  <option value="low">Low Priority</option>
                  <option value="medium">Medium Priority</option>
                  <option value="high">High Priority</option>
                </select>
                <input
                  type="date"
                  value={newTodo.due_date}
                  onChange={(e) => setNewTodo({ ...newTodo, due_date: e.target.value })}
                  className="w-full p-2 border rounded"
                />
                <button
                  type="submit"
                  className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                >
                  Create Todo
                </button>
              </form>
            </div>

            {/* Todo List */}
            <div className="md:col-span-2 bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-semibold mb-4">Your Todos</h2>
              <div className="space-y-4">
                {todos.map((todo) => (
                  <div
                    key={todo.id}
                    className={`border p-4 rounded ${
                      todo.completed ? "bg-gray-50" : "bg-white"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className={`font-semibold ${
                          todo.completed ? "line-through text-gray-500" : ""
                        }`}>
                          {todo.title}
                        </h3>
                        <p className="text-gray-600">{todo.description}</p>
                        <div className="mt-2 space-x-2">
                          <span className="text-sm text-gray-500">
                            Priority: {todo.priority}
                          </span>
                          {todo.due_date && (
                            <span className="text-sm text-gray-500">
                              Due: {todo.due_date}
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="space-x-2">
                        <button
                          onClick={() => handleToggleComplete(todo.id, todo.completed)}
                          className={`px-3 py-1 rounded ${
                            todo.completed
                              ? "bg-yellow-500 hover:bg-yellow-600"
                              : "bg-green-500 hover:bg-green-600"
                          } text-white`}
                        >
                          {todo.completed ? "Reopen" : "Complete"}
                        </button>
                        <button
                          onClick={() => handleDeleteTodo(todo.id)}
                          className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
      <CopilotSidebar />
    </CopilotKit>
  );
} 