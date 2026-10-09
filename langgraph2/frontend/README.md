# Hiring Workflow Frontend

This is the frontend application for the Hiring Workflow System, built with Next.js and CopilotKit.

## Features

- Modern, responsive UI with Tailwind CSS
- Resume upload with drag-and-drop support
- Real-time resume processing
- AI-powered resume screening results
- CopilotKit integration for enhanced AI capabilities
- Support for PDF, DOC, and DOCX resume formats

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file in the root directory with:
```
NEXT_PUBLIC_GROQ_API_KEY=your_groq_api_key_here
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── app/
│   ├── components/
│   ├── lib/
│   ├── globals.css
│   ├── layout.js
│   └── page.js
├── public/
├── next.config.js
├── tailwind.config.js
└── package.json
```

## Technologies Used

- Next.js 14
- React 18
- Tailwind CSS
- CopilotKit
- Groq LLM
- Axios
- React Dropzone

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint 