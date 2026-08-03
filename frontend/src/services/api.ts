import { AppSettings, Project, User } from '../types';

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
).replace(/\/$/, '');

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const payload = await response.json();
      if (typeof payload.detail === 'string') detail = payload.detail;
    } catch {
      // The server did not return JSON; use the status-based message.
    }
    throw new Error(detail);
  }
  return response.json() as Promise<T>;
}

export const api = {
  getProjects(): Promise<Project[]> {
    return request<Project[]>('/projects');
  },

  createProject(project: Partial<Project>): Promise<Project> {
    return request<Project>('/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(project),
    });
  },

  updateProjectStatus(projectId: string, status: string): Promise<Project> {
    return request<Project>(
      `/projects/${encodeURIComponent(projectId)}/status?status=${encodeURIComponent(status)}`,
      { method: 'PUT' },
    );
  },

  async deleteProject(id: string): Promise<void> {
    await request<{ message: string }>(`/projects/${encodeURIComponent(id)}`, {
      method: 'DELETE',
    });
  },

  getSettings(): Promise<AppSettings> {
    return request<AppSettings>('/settings');
  },

  updateSettings(settings: AppSettings): Promise<AppSettings> {
    return request<AppSettings>('/settings', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings),
    });
  },

  getDashboardStats(): Promise<{
    current_zone: string;
    focus_score: number;
    burnout_risk: string;
    deep_work_minutes: number;
    chart_data: { name: string; val: number }[];
  }> {
    return request('/activity/dashboard');
  },

  getLiveActivity(): Promise<{
    keystrokes: number;
    mouse_intensity: number;
    focus_score: number;
    cognitive_load: number;
    active_window: string;
    burnout_risk: string;
    context_switches: number;
  }> {
    return request('/activity/live');
  },

  getAnalyticsData(projectId: string | null, granularity: string): Promise<{
    label: string;
    focus: number;
    workload: number;
    cognitiveLoad: number;
    prevFocus: number;
    prevWorkload: number;
  }[]> {
    const query = new URLSearchParams({ granularity });
    if (projectId) query.append('project_id', projectId);
    return request(`/activity/analytics?${query.toString()}`);
  },

  async login(
    email: string,
    password: string,
  ): Promise<User & { accessToken: string }> {
    const data = await request<{ access_token: string }>('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return {
      name: email.split('@')[0],
      email,
      accessToken: data.access_token,
    };
  },

  async register(
    email: string,
    password: string,
    fullName?: string,
  ): Promise<User & { accessToken: string }> {
    const data = await request<{ access_token: string }>('/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name: fullName }),
    });
    return {
      name: fullName || email.split('@')[0],
      email,
      accessToken: data.access_token,
    };
  },
};
