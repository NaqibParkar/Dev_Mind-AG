import { Project, AppSettings, User, NavigationPage } from './types';

const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async getProjects(): Promise<Project[]> {
    const response = await fetch(`${API_BASE_URL}/projects`);
    if (!response.ok) throw new Error('Failed to fetch projects');
    return response.json();
  },

  async createProject(project: Partial<Project>): Promise<Project> {
    const response = await fetch(`${API_BASE_URL}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(project),
    });
    if (!response.ok) throw new Error('Failed to create project');
    return response.json();
  },

  async updateProjectStatus(projectId: string, status: string): Promise<Project> {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}/status?status=${status}`, {
      method: 'PUT',
    });
    if (!response.ok) throw new Error('Failed to update project status');
    return response.json();
  },

  async getSettings(): Promise<AppSettings> {
    const response = await fetch(`${API_BASE_URL}/settings`);
    if (!response.ok) throw new Error('Failed to fetch settings');
    return response.json();
  },

  async updateSettings(settings: AppSettings): Promise<AppSettings> {
    const response = await fetch(`${API_BASE_URL}/settings`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings),
    });
    if (!response.ok) throw new Error('Failed to update settings');
    return response.json();
  },

  async getLiveActivity(): Promise<{
    keystrokes: number;
    mouse_intensity: number;
    focus_score: number;
    cognitive_load: number;
    active_window: string;
  }> {
    const response = await fetch(`${API_BASE_URL}/activity/live`);
    if (!response.ok) throw new Error('Failed to fetch live activity');
    return response.json();
  },

  // Placeholder for Auth
  async login(): Promise<User> {
    // For now, just return a mock user
    return { name: 'Developer', email: 'dev@devmind.local' };
  }
};
