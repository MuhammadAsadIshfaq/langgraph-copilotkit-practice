"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  useCoAgent,
  useCoAgentStateRender,
  useCopilotAction,
} from "@copilotkit/react-core";
import { Progress } from "./Progress";
import { TaskList } from "./TaskList";
import { Task, AgentState } from "@/lib/types";

export function TodoManagement() {
  const { state, setState } = useCoAgent<AgentState>({
    name: "todo_agent",
    initialState: {
      model: "gpt-4",
      tasks: [],
      logs: [],
    },
  });

  useCoAgentStateRender({
    name: "todo_agent",
    render: ({ state, nodeName, status }) => {
      if (!state.logs || state.logs.length === 0) {
        return null;
      }
      return <Progress logs={state.logs} />;
    },
  });

  useCopilotAction({
    name: "DeleteTasks",
    description: "Delete selected tasks",
    available: "remote",
    parameters: [
      {
        name: "taskIds",
        type: "string[]",
      },
    ],
    renderAndWait: ({ args, status, handler }) => {
      return (
        <div className="p-4 bg-white rounded-lg shadow">
          <div className="font-bold text-base mb-2">
            Delete these tasks?
          </div>
          <TaskList
            tasks={state.tasks.filter((task) =>
              (args.taskIds || []).includes(task.id)
            )}
            onTaskClick={() => {}}
            onTaskDelete={() => {}}
          />
          {status === "executing" && (
            <div className="mt-4 flex justify-start space-x-2">
              <button
                onClick={() => handler("NO")}
                className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold"
              >
                Cancel
              </button>
              <button
                onClick={() => handler("YES")}
                className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
              >
                Delete
              </button>
            </div>
          )}
        </div>
      );
    },
  });

  const [newTask, setNewTask] = useState<Task>({
    id: "",
    title: "",
    description: "",
    status: "pending",
    priority: "medium",
  });

  const addTask = () => {
    if (newTask.title) {
      const taskWithId = {
        ...newTask,
        id: Date.now().toString(),
      };
      setState({
        ...state,
        tasks: [...state.tasks, taskWithId],
      });
      setNewTask({
        id: "",
        title: "",
        description: "",
        status: "pending",
        priority: "medium",
      });
    }
  };

  const handleTaskClick = (task: Task) => {
    setState({
      ...state,
      currentTask: task,
    });
  };

  const handleTaskDelete = (taskId: string) => {
    setState({
      ...state,
      tasks: state.tasks.filter((task) => task.id !== taskId),
    });
  };

  return (
    <div className="w-full h-full overflow-y-auto p-10 bg-[#F5F8FF]">
      <div className="space-y-8 pb-10">
        <div>
          <h2 className="text-lg font-medium mb-3 text-primary">
            New Task
          </h2>
          <div className="space-y-4">
            <Input
              placeholder="Task title"
              value={newTask.title}
              onChange={(e) =>
                setNewTask({ ...newTask, title: e.target.value })
              }
              className="bg-background px-4 py-2 border-0 shadow-none rounded-lg"
            />
            <Textarea
              placeholder="Task description"
              value={newTask.description}
              onChange={(e) =>
                setNewTask({ ...newTask, description: e.target.value })
              }
              className="bg-background px-4 py-2 border-0 shadow-none rounded-lg"
            />
            <button
              onClick={addTask}
              className="px-4 py-2 bg-[#6766FC] text-white rounded-lg font-medium"
            >
              Add Task
            </button>
          </div>
        </div>

        <div>
          <h2 className="text-lg font-medium mb-3 text-primary">
            Tasks
          </h2>
          <TaskList
            tasks={state.tasks}
            onTaskClick={handleTaskClick}
            onTaskDelete={handleTaskDelete}
          />
        </div>

        {state.currentTask && (
          <div>
            <h2 className="text-lg font-medium mb-3 text-primary">
              Current Task
            </h2>
            <div className="p-4 bg-white rounded-lg shadow">
              <h3 className="font-medium text-lg">{state.currentTask.title}</h3>
              <p className="mt-2 text-gray-600">{state.currentTask.description}</p>
              <div className="mt-4 flex items-center space-x-2">
                <span className={`px-2 py-1 rounded text-xs ${
                  state.currentTask.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {state.currentTask.status}
                </span>
                <span className={`px-2 py-1 rounded text-xs ${
                  state.currentTask.priority === 'high' ? 'bg-red-100 text-red-800' :
                  state.currentTask.priority === 'medium' ? 'bg-blue-100 text-blue-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {state.currentTask.priority}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
