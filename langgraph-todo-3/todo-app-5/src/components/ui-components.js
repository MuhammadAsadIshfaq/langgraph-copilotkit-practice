"use client"

import { useState } from "react"
import { Progress } from "@/components/ui/progress" // adjust import path

import { useFormStatus } from "react-dom"
import { useCopilotReadable } from "@copilotkit/react-core"; 


export function SubmitButton({ children, className = "" }) {
  const { pending } = useFormStatus()

  return (
    <button
      type="submit"
      disabled={pending}
      className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 ${className}`}
    >
      {pending ? "Loading..." : children}
    </button>
  )
}

export function FormMessage({ message }) {
  if (!message) return null

  const isError = message.error
  const text = isError ? message.error : message.success

  return <div className={`mt-2 text-sm ${isError ? "text-red-600" : "text-green-600"}`}>{text}</div>
}

export function TaskStatusBadge({ status }) {
  const colors = {
    TODO: "bg-gray-100 text-gray-800",
    IN_PROGRESS: "bg-blue-100 text-blue-800",
    COMPLETED: "bg-green-100 text-green-800",
  }

  const labels = {
    TODO: "To Do",
    IN_PROGRESS: "In Progress",
    COMPLETED: "Completed",
  }

  return <span className={`px-2 py-1 text-xs font-medium rounded-full ${colors[status]}`}>{labels[status]}</span>
}

export function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium">{title}</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            ✕
          </button>
        </div>
        {children}
      </div>
    </div>
  )
}

export function DeleteConfirmation({ onConfirm, onCancel, isDeleting }) {
  return (
    <div className="p-4 bg-red-50 rounded-lg">
      <p className="mb-4">Are you sure you want to delete this item? This action cannot be undone.</p>
      <div className="flex justify-end space-x-2">
        <button
          onClick={onCancel}
          className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
          disabled={isDeleting}
        >
          Cancel
        </button>
        <button
          onClick={onConfirm}
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          disabled={isDeleting}
        >
          {isDeleting ? "Deleting..." : "Delete"}
        </button>
      </div>
    </div>
  )
}

export function UserForm({ user, onSubmit, formState }) {
  const [formData, setFormData] = useState({
    id: user?.id || "",
    name: user?.name || "",
    email: user?.email || "",
    password: "",
    role: user?.role || "USER",
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="hidden" name="id" value={formData.id} />

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Name</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded"
          required
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded"
          required
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Password {user ? "(Leave blank to keep current)" : ""}</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded"
          required={!user}
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Role</label>
        <select name="role" value={formData.role} onChange={handleChange} className="w-full px-3 py-2 border rounded">
          <option value="USER">User</option>
          <option value="ADMIN">Admin</option>
        </select>
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          disabled={formState?.pending}
        >
          {formState?.pending ? "Saving..." : user ? "Update User" : "Create User"}
        </button>
      </div>

      {formState?.error && <div className="mt-2 text-sm text-red-600">{formState.error}</div>}
      {formState?.success && <div className="mt-2 text-sm text-green-600">{formState.success}</div>}
    </form>
  )
}

export function TaskForm({ task, users, onSubmit, formState }) {
  const [formData, setFormData] = useState({
    id: task?.id || "",
    title: task?.title || "",
    description: task?.description || "",
    status: task?.status || "TODO",
    assigneeId: task?.assigneeId || "",
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="hidden" name="id" value={formData.id} />

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Title</label>
        <input
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded"
          required
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Description</label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded"
          rows="3"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Status</label>
        <select
          name="status"
          value={formData.status}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded"
        >
          <option value="TODO">To Do</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="COMPLETED">Completed</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Assign To</label>
        <select
          name="assigneeId"
          value={formData.assigneeId}
          onChange={handleChange}
          className="w-full px-3 py-2 border rounded"
        >
          <option value="">Unassigned</option>
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.name} ({user.email})
            </option>
          ))}
        </select>
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          disabled={formState?.pending}
        >
          {formState?.pending ? "Saving..." : task ? "Update Task" : "Create Task"}
        </button>
      </div>

      {formState?.error && <div className="mt-2 text-sm text-red-600">{formState.error}</div>}
      {formState?.success && <div className="mt-2 text-sm text-green-600">{formState.success}</div>}
    </form>
  )
}
