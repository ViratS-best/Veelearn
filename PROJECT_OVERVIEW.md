# 🎓 Veelearn: Interactive STEM Learning Platform

Veelearn is a comprehensive, professional-grade educational platform designed for science, technology, engineering, and mathematics (STEM) education. It combines structured course management with powerful, interactive visual simulations and a community-driven marketplace.

---

## 🚀 Key Modules & Features

### 1. Advanced Course Creator & Viewer
The heart of the platform where educators can build rich, interactive learning experiences.
- **Dynamic Course Creation**: Educators can build courses with text, images, and interactive elements.
- **LaTeX Mathematical Support**: Full support for complex mathematical equations using LaTeX (Inline and Display modes) with a built-in snippet library and previewer.
- **Course Viewer**: A seamless student interface for consuming content, interacting with simulations, and taking quizzes.
- **Question Integration**: Ability to insert multiple-choice questions directly into the course flow.

### 2. Block Simulation Engine
A visual programming environment that allows students and teachers to create complex simulations without writing traditional code.
- **Topological Execution Engine**: Handles complex dependencies between simulation blocks.
- **60 FPS Rendering**: High-performance canvas-based rendering for smooth animations.
- **Interactive Parameters**: Real-time slider and input controls to modify simulation variables on the fly.
- **Physics Support**: Built-in support for gravity, collisions, springs, and motion dynamics.

### 3. Physics & Visual Simulator
Specialized toolsets for creating scientific visualizations.
- **Block-Based Physics**: Drag-and-drop blocks for defining physical properties and behaviors.
- **Visual Feedback**: Real-time visualization of forces, velocities, and object interactions.
- **Template System**: Pre-built templates for common physics scenarios (e.g., oscillating blocks, collisions).

### 4. Simulator Marketplace
A community hub for sharing and discovering simulations.
- **Discovery Engine**: Search and browse community-created simulators by category and popularity.
- **Forking/Remixing System**: Users can "fork" existing simulators to customize them and create their own versions.
- **Rating & Reviews**: Community feedback system for identifying the best resources.
- **Creator Dashboard**: Tools for managing shared simulators and tracking their performance.

### 5. PhET Integration
A library of over 120+ high-quality HTML5 interactive simulations from PhET Interactive Simulations (University of Colorado Boulder), categorized by subject:
- **Physics**: Quantum mechanics, electricity, motion, light.
- **Chemistry**: Atoms, molecules, states of matter.
- **Biology & Math**: Natural selection, graphing, geometry.

---

## 🛠️ Technical Architecture

### Backend (Node.js & Express)
- **RESTful API**: Handles authentication, course management, marketplace logic, and user data.
- **Security**: JWT-based authentication, bcrypt password hashing, and role-based access control (RBAC).
- **Database**: MySQL for structured data storage (users, courses, simulators, marketplace meta).
- **Architecture**: Service-oriented design with separate concerns for routes, database operations, and utility systems.

### Frontend (Vanilla JS, HTML5, CSS3)
- **High Performance**: No heavy frameworks; uses optimized vanilla JavaScript for maximum portability and performance.
- **Responsive Design**: Custom CSS system providing a premium "glassmorphism" aesthetic and mobile-ready layouts.
- **Engines**: 
    - `block-execution-engine.js`: The custom logic processor.
    - `block-physics-engine.js`: Handles delta-time based physics calculations.
    - `block-renderer-system.js`: Dedicated canvas rendering pipeline.

---

## 📁 Project Structure

### Root Directory
- Contains project-wide documentation and session-based development logs (Session 1 to 35+).
- `VEELEARN_PROJECT_OVERVIEW.md`: This document.
- `START_HERE.md`: The initial implementation roadmap.

### `veelearn-backend/`
- `server.js`: The main Express server and API entry point.
- `simulators.js`: Core logic for simulator management.
- `interactive-params-routes.js`: Management of simulation control variables.
- `test-db-connection.js`: Database diagnostic tool.

### `veelearn-frontend/`
- `index.html`: Main landing page and entry portal.
- `script.js`: Primary frontend logic coordinator.
- `block-simulator.html`: The visual programming interface.
- `visual-simulator.html`: High-level physics visualization tool.
- `simulator-marketplace.html`: The community discovery portal.
- `styles.css`: Central design system and aesthetics.

---

## 🌟 Technical Highlights
- **Performance**: Optimized to handle 1000+ particles at 60 FPS.
- **Extensibility**: Modular block system allows for easy addition of new simulation types.
- **SEO Ready**: Semantic HTML structure with proper metadata.
- **Security**: Parameterized SQL queries to prevent injection attacks.

---

## 📝 Ongoing Development
The project is maintained through iterative sessions. For detailed historical progress and specific bug fixes, refer to the `SESSION_XX_...md` files in the root directory.

*Current Status: Active Development / Version 2.0.0*
