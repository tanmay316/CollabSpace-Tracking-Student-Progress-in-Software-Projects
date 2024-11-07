<template>
    <div class="container">
      <div class="header"><h2>SWE: Project</h2></div>
      <div class="content">
        <div class="grid">

          <div class="project-card">
            <div class="card-header">
              <h3>
                <RouterLink to="/milestone">
                  <a
                  href=""
                  target="_blank"
                  rel="noreferrer"
                  >
                  Milestones
                </a>
              </RouterLink>
              </h3>
              <a class="badge"
                href="https://github.com/anigaut/soft-engg-project-sep-2024-se-sep-10"
                target="_blank"
                rel="noreferrer"
              >
              GitHub
            </a>
            </div>
            <div class="card-body">
              <div>
                <div class="milestones">🟢 Milestone 1</div>
                <div class="milestones">🟢 Milestone 2</div>
                <div class="milestones">🟢 Milestone 3</div>
                <div class="milestones">🔴 Milestone 4</div>
                <div class="milestones">🔴 Milestone 5</div>
                <div class="milestones">🔴 Milestone 6</div>
              </div>
            </div>
            <div class="card-footer">
              <div class="technologies">
                <span class="p1-dot"></span>
                <span class="label">Python</span>
                <span class="p2-dot"></span>
                <span class="label">Vue</span>
              </div>
              <div class="stats">
                <span>⭐ 2</span>
                <span>🍴 2</span>
              </div>
            </div>
          </div>

          <div class="project-card">
            <div class="card-header">
              <h3>
                <RouterLink to="/milestone">
                  <a
                  href=""
                  target="_blank"
                  rel="noreferrer"
                  >
                  Deadlines
                </a>
              </RouterLink>
            </h3>
            </div>
            <div class="card-body">
              <div>
                <div class="milestones">1</div>
                <div class="milestones">2</div>
                <div class="milestones">3</div>
                <div class="milestones">4</div>
                <div class="milestones">5</div>
                <div class="milestones">6</div>
              </div>
            </div>
          </div>

        </div>

        <div class="project-card">
            <div class="card-header">
              <h3>
                <RouterLink to="/milestone">
                  <a
                  href=""
                  target="_blank"
                  rel="noreferrer"
                  >
                  Viva Slots
                </a>
              </RouterLink>
              </h3>
              <span class="badge">
              Open
              </span>
            </div>
            <div class="card-body">
              <div class="slots">
                <div class="slot">Slot No. 1</div>
                <div class="slot">Slot No. 2</div>
                <div class="slot">Slot No. 3</div>
                <div class="slot">Slot No. 4</div>
                <div class="slot">Slot No. 5</div>
                <div class="slot">Slot No. 6</div>
              </div>
            </div>
          </div>

      </div>
    </div>
  </template>
  
  <style scoped>
  h2 {
  color: gray;
  font-weight: bold;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  }

  .slots{
    color: #000;
    display: flex;
    padding: 0.5rem;
  }
  
  .slot{
    color: #000;
    display: flex;
    padding: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin:0 0.5rem;
  }
  
  .slot:hover{
    cursor: pointer;
    transform: scale(1.05);
    background-color: #10b981;
  }
  
  .container {
    background-color: #f3f4f6;
    padding: 24px;
    margin-top: 5rem;
  }

  .milestones{
    color: black;
  }
  
  .header {
    text-align: center;
    font-size: 1.5rem;
    color: #000;
    padding-bottom: 48px;
  }
  
  .content {
    max-width: 64rem;
    margin: 0 auto;
  }
  
  .grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
    margin-bottom: 2rem;
  }
  
  @media (min-width: 640px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .project-card {
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    transition: transform 0.2s ease-in-out;
    overflow: hidden;
  }
  
  .project-card:hover {
    transform: scale(1.05);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .card-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
  }
  
  .card-header a {
    text-decoration: none;
    color: inherit;
  }
  
  .badge {
    background-color: #1f2937;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 4px 8px;
    border-radius: 9999px;
  }
  
  .card-body {
    padding: 16px;
  }
  
  .card-body p {
    color: #4b5563;
    font-size: 1rem;
  }
  
  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-top: 1px solid #e5e7eb;
  }
  
  .technologies {
    display: flex;
    align-items: center;
  }
  
  .p1-dot,
  .p2-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 8px;
  }
  
  .p1-dot {
    background-color: #06b6d4;
  }
  
  .p2-dot {
    background-color: #13cd73;
  }
  
  .label {
    font-size: 0.875rem;
    color: #374151;
    margin-right: 16px;
  }
  
  .stats {
    color: #6b7280;
    font-size: 0.875rem;
  }
  </style>
  