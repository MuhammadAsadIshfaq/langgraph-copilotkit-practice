export interface Task {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'completed';
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface AgentState {
  model: string;
  tasks: Task[];
  currentTask?: Task;
  logs: string[];
  research_question?: string;
  report?: string;
}

export interface Resource {
  url: string;
  title: string;
  description: string;
} 