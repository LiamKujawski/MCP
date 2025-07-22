'use client';

import { useState, useEffect } from 'react';
import { 
  Card, CardContent, CardDescription, CardHeader, CardTitle,
  Button,
  Tabs, TabsContent, TabsList, TabsTrigger,
  Input,
  Label,
  Textarea,
  Alert, AlertDescription,
  Badge,
  Progress
} from '@/components/ui/components';
import {
  PlayCircle,
  PauseCircle,
  RefreshCw,
  Upload,
  Download,
  FileText,
  GitBranch,
  Activity,
  CheckCircle2,
  XCircle,
  Clock,
  Zap,
  FolderPlus,
  FileSearch,
  Rocket,
  Settings,
  Home,
  AlertCircle,
  Loader2
} from 'lucide-react';

interface WorkflowStatus {
  workflow_id: string;
  status: string;
  phases_completed: string[];
  current_phase: string;
  error?: string;
  metadata?: any;
}

interface ResearchTopic {
  name: string;
  description: string;
  files: string[];
  status: 'pending' | 'processing' | 'completed' | 'error';
  lastModified: string;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [workflowStatus, setWorkflowStatus] = useState<WorkflowStatus | null>(null);
  const [researchTopics, setResearchTopics] = useState<ResearchTopic[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [newTopicForm, setNewTopicForm] = useState({
    name: '',
    description: '',
    content: ''
  });
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [pipelineProgress, setPipelineProgress] = useState(0);
  const [agents, setAgents] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any>(null);

  // Fetch initial data
  useEffect(() => {
    fetchResearchTopics();
    fetchAgents();
    fetchMetrics();
  }, []);

  // Poll for workflow status when active
  useEffect(() => {
    if (workflowStatus && workflowStatus.status === 'processing') {
      const interval = setInterval(() => {
        checkWorkflowStatus(workflowStatus.workflow_id);
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [workflowStatus]);

  const fetchResearchTopics = async () => {
    try {
      const response = await fetch('http://localhost:8000/research/topics');
      const data = await response.json();
      
      // Transform backend data to match our interface
      const topics = data.topics.map((topic: any) => ({
        name: topic.name,
        description: topic.description || 'No description available',
        files: topic.files,
        status: 'completed' as const, // Default status
        lastModified: new Date().toISOString()
      }));
      
      setResearchTopics(topics);
    } catch (err) {
      console.error('Error fetching research topics:', err);
      // Fallback to sample data if backend is not available
      setResearchTopics([
        {
          name: 'Multi-Agent Collaboration',
          description: 'Research on multi-agent systems and collaboration patterns',
          files: ['01_overview.md', '02_architecture.md', '03_prompt_design.md'],
          status: 'completed',
          lastModified: new Date().toISOString()
        }
      ]);
    }
  };

  const fetchAgents = async () => {
    try {
      const response = await fetch('http://localhost:8000/agents');
      const data = await response.json();
      setAgents(data.agents || []);
    } catch (err) {
      console.error('Error fetching agents:', err);
    }
  };

  const fetchMetrics = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      console.error('Error fetching metrics:', err);
    }
  };

  const startWorkflow = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    setPipelineProgress(10);

    try {
      const response = await fetch('http://localhost:8000/workflow/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          description: selectedTopic 
            ? `Process research topic: ${selectedTopic}`
            : 'Run complete research synthesis pipeline'
        })
      });

      if (!response.ok) {
        throw new Error('Failed to start workflow');
      }

      const data = await response.json();
      setWorkflowStatus(data);
      setSuccess('Workflow started successfully!');
      setPipelineProgress(25);
    } catch (err: any) {
      setError(err.message || 'Failed to start workflow');
      setPipelineProgress(0);
    } finally {
      setLoading(false);
    }
  };

  const checkWorkflowStatus = async (workflowId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/workflow/${workflowId}/status`);
      const data = await response.json();
      setWorkflowStatus(data);
      
      // Update progress based on phases completed
      const progress = (data.phases_completed.length / 5) * 100;
      setPipelineProgress(progress);
      
      if (data.status === 'completed') {
        setSuccess('Workflow completed successfully!');
      } else if (data.status === 'failed') {
        setError('Workflow failed: ' + (data.error || 'Unknown error'));
        setPipelineProgress(0);
      }
    } catch (err) {
      console.error('Error checking workflow status:', err);
    }
  };

  const createNewTopic = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch('http://localhost:8000/research/topics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newTopicForm.name,
          description: newTopicForm.description,
          content: newTopicForm.content
        })
      });

      if (!response.ok) {
        throw new Error('Failed to create research topic');
      }

      const data = await response.json();
      
      // Add the new topic to our list
      const newTopic: ResearchTopic = {
        name: newTopicForm.name,
        description: newTopicForm.description,
        files: data.files,
        status: 'pending',
        lastModified: new Date().toISOString()
      };

      setResearchTopics([...researchTopics, newTopic]);
      setSuccess(`Research topic "${newTopicForm.name}" created successfully!`);
      
      // Reset form
      setNewTopicForm({ name: '', description: '', content: '' });
      
      // Refresh the topics list
      setTimeout(fetchResearchTopics, 1000);
    } catch (err: any) {
      setError(err.message || 'Failed to create research topic');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      case 'processing':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'error':
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: any = {
      completed: 'success',
      processing: 'secondary',
      error: 'destructive',
      failed: 'destructive',
      pending: 'outline'
    };
    
    return <Badge variant={variants[status] || 'outline'}>{status}</Badge>;
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Zap className="w-8 h-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                MCP Control Center
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => window.location.href = '/'}
              >
                <Home className="w-4 h-4 mr-2" />
                Home
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => window.open('http://localhost:8000/docs', '_blank')}
              >
                <FileText className="w-4 h-4 mr-2" />
                API Docs
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Alerts */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        
        {success && (
          <Alert className="mb-6 border-green-200 bg-green-50 text-green-800">
            <CheckCircle2 className="h-4 w-4" />
            <AlertDescription>{success}</AlertDescription>
          </Alert>
        )}

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="research">Research</TabsTrigger>
            <TabsTrigger value="pipeline">Pipeline</TabsTrigger>
            <TabsTrigger value="agents">Agents</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Total Research Topics
                  </CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{researchTopics.length}</div>
                  <p className="text-xs text-muted-foreground">
                    {researchTopics.filter(t => t.status === 'completed').length} completed
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Active Agents
                  </CardTitle>
                  <Activity className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{agents.length}</div>
                  <p className="text-xs text-muted-foreground">
                    Ready to process
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Pipeline Status
                  </CardTitle>
                  <Rocket className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {workflowStatus ? workflowStatus.status : 'Idle'}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {workflowStatus?.current_phase || 'Ready to start'}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    System Health
                  </CardTitle>
                  <Activity className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {metrics?.status === 'healthy' ? 'Healthy' : 'Unknown'}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    All systems operational
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
                <CardDescription>
                  Common tasks you can perform with a single click
                </CardDescription>
              </CardHeader>
              <CardContent className="grid grid-cols-2 gap-4">
                <Button
                  onClick={startWorkflow}
                  disabled={loading}
                  className="flex items-center justify-center"
                >
                  {loading ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    <PlayCircle className="mr-2 h-4 w-4" />
                  )}
                  Start Full Pipeline
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setActiveTab('research')}
                  className="flex items-center justify-center"
                >
                  <FolderPlus className="mr-2 h-4 w-4" />
                  Create Research Topic
                </Button>
                <Button
                  variant="outline"
                  onClick={fetchResearchTopics}
                  className="flex items-center justify-center"
                >
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Refresh Status
                </Button>
                <Button
                  variant="outline"
                  onClick={() => window.open('/api-docs', '_blank')}
                  className="flex items-center justify-center"
                >
                  <FileSearch className="mr-2 h-4 w-4" />
                  View Documentation
                </Button>
              </CardContent>
            </Card>

            {/* Pipeline Progress */}
            {workflowStatus && (
              <Card>
                <CardHeader>
                  <CardTitle>Pipeline Progress</CardTitle>
                  <CardDescription>
                    Current workflow execution status
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">
                      Workflow ID: {workflowStatus.workflow_id}
                    </span>
                    {getStatusBadge(workflowStatus.status)}
                  </div>
                  <Progress value={pipelineProgress} className="w-full" />
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium">Phases:</h4>
                    <div className="grid grid-cols-5 gap-2">
                      {['Research', 'Synthesis', 'Experiment', 'Deploy', 'Optimize'].map((phase) => (
                        <div
                          key={phase}
                          className={`text-center p-2 rounded ${
                            workflowStatus.phases_completed.includes(phase.toLowerCase())
                              ? 'bg-green-100 text-green-800'
                              : workflowStatus.current_phase === phase.toLowerCase()
                              ? 'bg-blue-100 text-blue-800'
                              : 'bg-gray-100 text-gray-500'
                          }`}
                        >
                          <span className="text-xs">{phase}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Research Tab */}
          <TabsContent value="research" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Research Topics</CardTitle>
                <CardDescription>
                  Manage your research topics and create new ones
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {/* Existing Topics */}
                  <div className="space-y-2">
                    {researchTopics.map((topic) => (
                      <div
                        key={topic.name}
                        className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
                      >
                        <div className="flex items-center space-x-4">
                          {getStatusIcon(topic.status)}
                          <div>
                            <h4 className="font-medium">{topic.name}</h4>
                            <p className="text-sm text-gray-500">{topic.description}</p>
                            <p className="text-xs text-gray-400">
                              {topic.files.length} files • Last modified: {new Date(topic.lastModified).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              setSelectedTopic(topic.name);
                              setActiveTab('pipeline');
                            }}
                          >
                            <Rocket className="w-4 h-4 mr-2" />
                            Process
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Create New Topic */}
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-medium mb-4">Create New Research Topic</h3>
                    <div className="space-y-4">
                      <div>
                        <Label htmlFor="topic-name">Topic Name</Label>
                        <Input
                          id="topic-name"
                          placeholder="e.g., Advanced Prompt Engineering"
                          value={newTopicForm.name}
                          onChange={(e) => setNewTopicForm({...newTopicForm, name: e.target.value})}
                        />
                      </div>
                      <div>
                        <Label htmlFor="topic-description">Description</Label>
                        <Input
                          id="topic-description"
                          placeholder="Brief description of the research topic"
                          value={newTopicForm.description}
                          onChange={(e) => setNewTopicForm({...newTopicForm, description: e.target.value})}
                        />
                      </div>
                      <div>
                        <Label htmlFor="topic-content">Initial Content (Markdown)</Label>
                        <Textarea
                          id="topic-content"
                          placeholder="Enter your research content in markdown format..."
                          rows={10}
                          value={newTopicForm.content}
                          onChange={(e) => setNewTopicForm({...newTopicForm, content: e.target.value})}
                        />
                      </div>
                      <Button
                        onClick={createNewTopic}
                        disabled={loading || !newTopicForm.name || !newTopicForm.content}
                      >
                        {loading ? (
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        ) : (
                          <FolderPlus className="mr-2 h-4 w-4" />
                        )}
                        Create Research Topic
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Pipeline Tab */}
          <TabsContent value="pipeline" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Pipeline Control</CardTitle>
                <CardDescription>
                  Manage and monitor the research synthesis pipeline
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Pipeline Options */}
                <div className="space-y-4">
                  <div>
                    <Label>Select Research Topic (Optional)</Label>
                    <select
                      className="w-full mt-2 p-2 border rounded-md"
                      value={selectedTopic || ''}
                      onChange={(e) => setSelectedTopic(e.target.value || null)}
                    >
                      <option value="">Process all topics</option>
                      {researchTopics.map((topic) => (
                        <option key={topic.name} value={topic.name}>
                          {topic.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="flex space-x-4">
                    <Button
                      onClick={startWorkflow}
                      disabled={loading || (workflowStatus?.status === 'processing')}
                      size="lg"
                      className="flex-1"
                    >
                      {loading ? (
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      ) : (
                        <PlayCircle className="mr-2 h-5 w-5" />
                      )}
                      Start Pipeline
                    </Button>
                    
                    {workflowStatus?.status === 'processing' && (
                      <Button
                        variant="destructive"
                        size="lg"
                        onClick={() => {
                          // In production, this would call an endpoint to stop the workflow
                          setWorkflowStatus({...workflowStatus, status: 'stopped'});
                          setPipelineProgress(0);
                        }}
                      >
                        <PauseCircle className="mr-2 h-5 w-5" />
                        Stop Pipeline
                      </Button>
                    )}
                  </div>
                </div>

                {/* Pipeline Visualization */}
                <div className="border rounded-lg p-6">
                  <h3 className="text-lg font-medium mb-4">Pipeline Flow</h3>
                  <div className="space-y-4">
                    {[
                      { 
                        phase: 'Research', 
                        description: 'Collect and normalize research documents',
                        icon: <FileSearch className="w-5 h-5" />
                      },
                      { 
                        phase: 'Synthesis', 
                        description: 'AI generates implementation prompts',
                        icon: <GitBranch className="w-5 h-5" />
                      },
                      { 
                        phase: 'Experiment', 
                        description: 'Execute models and run tests',
                        icon: <Activity className="w-5 h-5" />
                      },
                      { 
                        phase: 'Deploy', 
                        description: 'Containerize and deploy applications',
                        icon: <Rocket className="w-5 h-5" />
                      },
                      { 
                        phase: 'Optimize', 
                        description: 'Monitor performance and iterate',
                        icon: <Settings className="w-5 h-5" />
                      }
                    ].map((phase, index) => {
                      const isCompleted = workflowStatus?.phases_completed.includes(phase.phase.toLowerCase());
                      const isCurrent = workflowStatus?.current_phase === phase.phase.toLowerCase();
                      const isPending = !isCompleted && !isCurrent;

                      return (
                        <div key={phase.phase} className="flex items-center space-x-4">
                          <div className={`
                            flex items-center justify-center w-10 h-10 rounded-full
                            ${isCompleted ? 'bg-green-100 text-green-600' : 
                              isCurrent ? 'bg-blue-100 text-blue-600' : 
                              'bg-gray-100 text-gray-400'}
                          `}>
                            {phase.icon}
                          </div>
                          <div className="flex-1">
                            <h4 className={`font-medium ${isPending ? 'text-gray-400' : ''}`}>
                              {phase.phase}
                            </h4>
                            <p className="text-sm text-gray-500">{phase.description}</p>
                          </div>
                          <div>
                            {isCompleted && <CheckCircle2 className="w-5 h-5 text-green-500" />}
                            {isCurrent && <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />}
                            {isPending && <Clock className="w-5 h-5 text-gray-400" />}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Workflow Logs */}
                {workflowStatus && (
                  <div className="border rounded-lg p-4 bg-gray-50 dark:bg-gray-800">
                    <h3 className="text-sm font-medium mb-2">Workflow Logs</h3>
                    <pre className="text-xs overflow-auto max-h-40">
                      {JSON.stringify(workflowStatus, null, 2)}
                    </pre>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Agents Tab */}
          <TabsContent value="agents" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>AI Agents</CardTitle>
                <CardDescription>
                  View and manage the AI agents in the system
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {agents.map((agent) => (
                    <div key={agent.name} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-medium">{agent.name}</h3>
                        <Badge variant="outline">Active</Badge>
                      </div>
                      <p className="text-sm text-gray-500 mb-4">{agent.description}</p>
                      <div className="space-y-1 text-xs">
                        <p><span className="font-medium">Role:</span> {agent.role}</p>
                        <p><span className="font-medium">Capabilities:</span> {agent.capabilities?.join(', ') || 'N/A'}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Settings</CardTitle>
                <CardDescription>
                  Configure the MCP platform
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium mb-4">API Keys</h3>
                  <Alert>
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      API keys are configured in the .env file. Restart the application after making changes.
                    </AlertDescription>
                  </Alert>
                </div>

                <div>
                  <h3 className="text-lg font-medium mb-4">System Information</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Backend URL:</span>
                      <span className="font-mono">http://localhost:8000</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Frontend URL:</span>
                      <span className="font-mono">http://localhost:3000</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">API Documentation:</span>
                      <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        View Docs
                      </a>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-medium mb-4">Quick Links</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <Button variant="outline" onClick={() => window.open('https://github.com/LiamKujawski/MCP', '_blank')}>
                      <GitBranch className="mr-2 h-4 w-4" />
                      GitHub Repository
                    </Button>
                    <Button variant="outline" onClick={() => window.open('/docs', '_blank')}>
                      <FileText className="mr-2 h-4 w-4" />
                      Documentation
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}