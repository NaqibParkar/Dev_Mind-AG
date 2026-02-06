import { Project, MockDataPoint, Insight, CognitiveState, AppSettings, TimeGranularity } from './types';

export const MOCK_PROJECTS: Project[] = [
  { 
    id: '1', 
    name: 'Backend API Refactor', 
    description: 'Migrating legacy endpoints to GraphQL and optimizing DB queries.',
    color: 'bg-indigo-500', 
    timeSpentMinutes: 320, 
    avgFocusScore: 85, 
    workload: 78,
    status: 'Active' 
  },
  { 
    id: '2', 
    name: 'UI Component Lib', 
    description: 'Building a consistent design system with React & Tailwind.',
    color: 'bg-teal-400', 
    timeSpentMinutes: 145, 
    avgFocusScore: 92, 
    workload: 45,
    status: 'Inactive' 
  },
  { 
    id: '3', 
    name: 'Research & Docs', 
    description: 'Compiling technical documentation for the new architecture.',
    color: 'bg-purple-400', 
    timeSpentMinutes: 90, 
    avgFocusScore: 65, 
    workload: 30,
    status: 'Inactive' 
  },
];

// Hourly Data (Today)
export const MOCK_HOURLY_DATA: MockDataPoint[] = [
  { label: '09:00', focus: 85, workload: 35, cognitiveLoad: 40, prevFocus: 70, prevWorkload: 40 },
  { label: '10:00', focus: 92, workload: 55, cognitiveLoad: 65, prevFocus: 75, prevWorkload: 50 },
  { label: '11:00', focus: 78, workload: 70, cognitiveLoad: 80, prevFocus: 60, prevWorkload: 60 },
  { label: '12:00', focus: 45, workload: 25, cognitiveLoad: 30, prevFocus: 50, prevWorkload: 30 },
  { label: '13:00', focus: 88, workload: 60, cognitiveLoad: 70, prevFocus: 80, prevWorkload: 55 },
  { label: '14:00', focus: 65, workload: 85, cognitiveLoad: 85, prevFocus: 70, prevWorkload: 75 },
  { label: '15:00', focus: 55, workload: 80, cognitiveLoad: 90, prevFocus: 65, prevWorkload: 60 },
];

// Daily Data (This Week)
export const MOCK_DAILY_DATA: MockDataPoint[] = [
  { label: 'Mon', focus: 72, workload: 60, cognitiveLoad: 55, prevFocus: 68, prevWorkload: 65 },
  { label: 'Tue', focus: 85, workload: 75, cognitiveLoad: 70, prevFocus: 70, prevWorkload: 60 },
  { label: 'Wed', focus: 60, workload: 40, cognitiveLoad: 30, prevFocus: 75, prevWorkload: 50 },
  { label: 'Thu', focus: 90, workload: 85, cognitiveLoad: 80, prevFocus: 80, prevWorkload: 70 },
  { label: 'Fri', focus: 78, workload: 55, cognitiveLoad: 50, prevFocus: 72, prevWorkload: 55 },
  { label: 'Sat', focus: 45, workload: 20, cognitiveLoad: 20, prevFocus: 50, prevWorkload: 25 },
  { label: 'Sun', focus: 50, workload: 25, cognitiveLoad: 25, prevFocus: 40, prevWorkload: 30 },
];

// Helper to generate dynamic weekly data for the current month
const getWeeklyData = (): MockDataPoint[] => {
  const now = new Date();
  const currentDay = now.getDate();
  const month = now.toLocaleString('default', { month: 'short' });
  const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  
  // Define week ranges with specific IDs
  const weeks = [
    { id: 1, start: 1, end: 7, label: 'Week 1' },
    { id: 2, start: 8, end: 14, label: 'Week 2' },
    { id: 3, start: 15, end: 21, label: 'Week 3' },
    { id: 4, start: 22, end: lastDay, label: 'Week 4' },
  ];

  // Base mock values for the weeks
  const mockValues: Record<number, Omit<MockDataPoint, 'label'>> = {
    1: { focus: 75, workload: 65, cognitiveLoad: 60, prevFocus: 70, prevWorkload: 60 },
    2: { focus: 82, workload: 70, cognitiveLoad: 65, prevFocus: 72, prevWorkload: 65 },
    3: { focus: 68, workload: 55, cognitiveLoad: 50, prevFocus: 75, prevWorkload: 60 },
    4: { focus: 88, workload: 80, cognitiveLoad: 75, prevFocus: 80, prevWorkload: 70 },
  };

  return weeks.map(week => {
    // If the week hasn't started yet (current date is before the start of the week),
    // return zeroed-out data to represent "future".
    if (currentDay < week.start) {
        return {
            label: week.label,
            focus: 0,
            workload: 0,
            cognitiveLoad: 0,
            prevFocus: 0,
            prevWorkload: 0
        };
    }

    // If current date is within the week or past it, return data
    return {
        label: week.label,
        ...mockValues[week.id]
    };
  });
};

// Weekly Data (Current Month)
export const MOCK_WEEKLY_DATA: MockDataPoint[] = getWeeklyData();

export const CURRENT_STATE: CognitiveState = {
  currentZone: 'Optimal Focus',
  focusScore: 84,
  burnoutRisk: 'Low',
  focusStability: 92,
  deepWorkMinutes: 210,
};

export const INSIGHTS: Insight[] = [
  { id: '1', type: 'positive', title: 'Peak Performance', description: 'You maintained "Deep Work" for 55 minutes straight this morning.' },
  { id: '2', type: 'warning', title: 'Cognitive Load Spike', description: 'Context switching increased by 15% between 14:00 and 15:00.' },
];

export const EMOJI_OPTIONS = ['🤯', '😫', '😐', '🙂', '🧠'];

export const DEFAULT_COGNITIVE_DATA = [
  { name: '09:00', val: 30 },
  { name: '10:00', val: 45 },
  { name: '11:00', val: 65 },
  { name: '12:00', val: 50 },
  { name: '13:00', val: 40 },
  { name: '14:00', val: 70 },
  { name: '15:00', val: 85 },
  { name: '16:00', val: 60 },
];

export const MOCK_PROJECT_COGNITIVE_DATA: Record<string, { name: string; val: number }[]> = {
  '1': [
    { name: '09:00', val: 40 },
    { name: '10:00', val: 55 },
    { name: '11:00', val: 80 },
    { name: '12:00', val: 60 },
    { name: '13:00', val: 45 },
    { name: '14:00', val: 75 },
    { name: '15:00', val: 90 },
    { name: '16:00', val: 70 },
  ],
  '2': [
    { name: '09:00', val: 20 },
    { name: '10:00', val: 30 },
    { name: '11:00', val: 45 },
    { name: '12:00', val: 35 },
    { name: '13:00', val: 25 },
    { name: '14:00', val: 40 },
    { name: '15:00', val: 50 },
    { name: '16:00', val: 30 },
  ],
  '3': [
    { name: '09:00', val: 15 },
    { name: '10:00', val: 20 },
    { name: '11:00', val: 25 },
    { name: '12:00', val: 20 },
    { name: '13:00', val: 15 },
    { name: '14:00', val: 30 },
    { name: '15:00', val: 35 },
    { name: '16:00', val: 25 },
  ],
};

export const DEFAULT_SETTINGS: AppSettings = {
  smartBreaks: true,
  comparativeMode: true,
  reflectionJournal: true,
  passiveMode: false,
  alerts: {
    enabled: true,
    sensitivity: 'Medium',
    types: {
      burnout: true,
      focusDrop: true,
      contextSwitching: true,
      prolongedWork: true
    }
  }
};

/**
 * Generates specific analytics data for projects to simulate realistic
 * variations between different work contexts.
 */
export const getProjectAnalyticsData = (projectId: string | null, granularity: TimeGranularity): MockDataPoint[] => {
  let data: MockDataPoint[] = [];
  
  // Clone base data to avoid reference mutations across renders
  switch (granularity) {
    case 'hourly': data = MOCK_HOURLY_DATA.map(i => ({...i})); break;
    case 'daily': data = MOCK_DAILY_DATA.map(i => ({...i})); break;
    case 'weekly': data = MOCK_WEEKLY_DATA.map(i => ({...i})); break;
    default: data = MOCK_HOURLY_DATA.map(i => ({...i}));
  }

  if (!projectId) return data;

  // Define unique characteristics for mock projects
  // Format: { focus: adjustment, workload: adjustment }
  const modifiers: Record<string, { focus: number, workload: number }> = {
    '1': { focus: 5, workload: 15 },    // Backend: High Load
    '2': { focus: 10, workload: -10 },  // UI: High Focus, Lower Load
    '3': { focus: -15, workload: -20 }, // Research: Lower Focus/Load
  };

  const mod = modifiers[projectId] || { focus: 0, workload: 0 };
  const seed = projectId.charCodeAt(0) || 0;

  return data.map((item, index) => {
    // Pseudo-random variance based on index and project seed
    const variance = Math.sin(index + seed) * 10;
    
    // Apply modifiers and clamp values between 10 and 100
    const newFocus = Math.min(100, Math.max(10, item.focus + mod.focus + variance));
    const newWorkload = Math.min(100, Math.max(10, item.workload + mod.workload + (variance * -1))); // Inverse variance for workload
    
    return {
      ...item,
      focus: Math.round(newFocus),
      workload: Math.round(newWorkload),
      cognitiveLoad: Math.round((newFocus + newWorkload) / 2),
      // Adjust comparative data similarly
      prevFocus: item.prevFocus ? Math.min(100, Math.max(10, item.prevFocus + mod.focus)) : undefined,
      prevWorkload: item.prevWorkload ? Math.min(100, Math.max(10, item.prevWorkload + mod.workload)) : undefined,
    };
  });
};