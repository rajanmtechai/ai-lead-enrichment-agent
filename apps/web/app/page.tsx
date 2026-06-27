'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import { ArrowRight, BadgeCheck, Brain, Search, ShieldCheck, Sparkles, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

type Draft = {
  id: number;
  kind: string;
  status: string;
  subject_lines: string[];
  content: Record<string, unknown>;
  notes: string;
  crm_sync_status: string;
};

type CompanyProfile = {
  company: {
    id: number;
    domain: string;
    name: string;
    industry: string;
    description: string;
    icp_score: number;
    executives: Array<{ id: number; full_name: string; title: string; linkedin_url?: string | null }>;
    drafts: Draft[];
  };
  insights: {
    icp_score: number;
    buying_signals: string[];
    pain_points: string[];
    recommendations: string[];
    summary: string;
    signal_reasoning: string[];
  };
};

type Analytics = { companies: number; drafts: number; approved: number; synced: number };

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function Page() {
  const [token, setToken] = useState('');
  const [email, setEmail] = useState('admin@acme.com');
  const [password, setPassword] = useState('admin123!');
  const [query, setQuery] = useState('acme.com');
  const [profile, setProfile] = useState<CompanyProfile | null>(null);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);
  const [message, setMessage] = useState('Ready to research a new account.');

  useEffect(() => {
    const stored = window.localStorage.getItem('ai-lead-token');
    if (stored) {
      setToken(stored);
      void fetchAnalytics(stored);
    }
  }, []);

  const isAuthenticated = Boolean(token);

  async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
    const response = await fetch(`${apiUrl}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(init?.headers ?? {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
    if (!response.ok) {
      throw new Error(await response.text());
    }
    return response.json() as Promise<T>;
  }

  async function fetchAnalytics(authToken: string = token) {
    if (!authToken) return;
    const response = await fetch(`${apiUrl}/api/v1/analytics/overview`, {
      headers: { Authorization: `Bearer ${authToken}` },
    });
    if (response.ok) {
      setAnalytics((await response.json()) as Analytics);
    }
  }

  async function handleLogin(event: FormEvent) {
    event.preventDefault();
    setLoginLoading(true);
    try {
      const data = await fetchJson<{ access_token: string }>('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      window.localStorage.setItem('ai-lead-token', data.access_token);
      setToken(data.access_token);
      setMessage('Authenticated. Ready for research runs.');
      await fetchAnalytics(data.access_token);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Login failed');
    } finally {
      setLoginLoading(false);
    }
  }

  async function handleResearch(event: FormEvent) {
    event.preventDefault();
    if (!token) {
      setMessage('Sign in first to start a research run.');
      return;
    }
    setLoading(true);
    try {
      const data = await fetchJson<CompanyProfile>('/api/v1/research/company', {
        method: 'POST',
        body: JSON.stringify({ query }),
      });
      setProfile(data);
      setMessage(`Research complete for ${data.company.name}. Review the insights and drafts below.`);
      await fetchAnalytics();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Research failed');
    } finally {
      setLoading(false);
    }
  }

  async function approveDraft(draftId: number) {
    try {
      await fetchJson(`/api/v1/drafts/${draftId}/approve`, {
        method: 'POST',
        body: JSON.stringify({ notes: 'Approved from dashboard review' }),
      });
      setMessage(`Draft ${draftId} approved.`);
      if (profile) {
        const drafts = profile.company.drafts.map((draft) => (draft.id === draftId ? { ...draft, status: 'approved' } : draft));
        setProfile({ ...profile, company: { ...profile.company, drafts } });
      }
      await fetchAnalytics();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Approval failed');
    }
  }

  async function syncDraft(draftId: number) {
    try {
      await fetchJson(`/api/v1/drafts/${draftId}/sync`, { method: 'POST' });
      setMessage(`Draft ${draftId} queued for CRM sync.`);
      if (profile) {
        const drafts = profile.company.drafts.map((draft) => (draft.id === draftId ? { ...draft, crm_sync_status: 'queued' } : draft));
        setProfile({ ...profile, company: { ...profile.company, drafts } });
      }
      await fetchAnalytics();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Sync failed');
    }
  }

  const heroStats = useMemo(
    () => [
      { label: 'Company profile', value: profile?.company.name ?? 'Waiting for research' },
      { label: 'ICP score', value: profile ? `${profile.insights.icp_score.toFixed(0)}/100` : '—' },
      { label: 'Executive targets', value: profile?.company.executives.length?.toString() ?? '0' },
    ],
    [profile],
  );

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-8 px-4 py-6 sm:px-6 lg:px-8">
      <section className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
        <Card className="overflow-hidden border-white/12 bg-white/6">
          <CardBody className="relative flex flex-col gap-8 p-8">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(249,115,22,0.16),transparent_36%)]" />
            <div className="relative flex items-center justify-between gap-4">
              <div>
                <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-orange-400/30 bg-orange-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-orange-200">
                  <Sparkles className="h-3.5 w-3.5" /> Autonomous lead intelligence
                </div>
                <h1 className="max-w-2xl text-4xl font-semibold tracking-tight text-white sm:text-5xl">
                  Research accounts, generate outreach, and gate every send behind human approval.
                </h1>
                <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-300 sm:text-base">
                  Capture company signals, enrich executives, score ICP fit, and convert the research into outreach drafts ready for review and CRM sync.
                </p>
              </div>
              <div className="hidden rounded-3xl border border-white/10 bg-slate-950/40 p-4 shadow-glow lg:block">
                <ShieldCheck className="h-7 w-7 text-orange-300" />
              </div>
            </div>

            <div className="relative grid gap-3 sm:grid-cols-3">
              {heroStats.map((item) => (
                <Card key={item.label} className="border-white/10 bg-slate-950/30">
                  <CardBody className="space-y-2 p-4">
                    <div className="text-xs uppercase tracking-[0.22em] text-slate-400">{item.label}</div>
                    <div className="text-lg font-semibold text-white">{item.value}</div>
                  </CardBody>
                </Card>
              ))}
            </div>
          </CardBody>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 text-sm font-semibold text-white"><BadgeCheck className="h-4 w-4 text-orange-300" /> Authentication</div>
            </CardHeader>
            <CardBody>
              {isAuthenticated ? (
                <div className="space-y-2 text-sm text-slate-300">
                  <p>Signed in and ready to run research.</p>
                  <p className="text-xs text-slate-400">Token stored locally for development workflows.</p>
                </div>
              ) : (
                <form className="space-y-3" onSubmit={handleLogin}>
                  <Input value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Email" type="email" />
                  <Input value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Password" type="password" />
                  <Button type="submit" className="w-full bg-orange-500 text-white hover:bg-orange-400">
                    {loginLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                    Sign in
                  </Button>
                </form>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 text-sm font-semibold text-white"><Brain className="h-4 w-4 text-orange-300" /> Analytics</div>
            </CardHeader>
            <CardBody className="grid grid-cols-2 gap-3 text-sm">
              {analytics ? (
                Object.entries(analytics).map(([label, value]) => (
                  <div key={label} className="rounded-2xl border border-white/10 bg-black/20 p-3">
                    <div className="text-xs uppercase tracking-[0.2em] text-slate-400">{label}</div>
                    <div className="mt-2 text-lg font-semibold text-white">{value}</div>
                  </div>
                ))
              ) : (
                <div className="col-span-2 rounded-2xl border border-dashed border-white/10 p-6 text-slate-400">Run a research job to populate analytics.</div>
              )}
            </CardBody>
          </Card>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[0.7fr_1.3fr]">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-semibold text-white"><Search className="h-4 w-4 text-orange-300" /> Research</div>
          </CardHeader>
          <CardBody>
            <form className="space-y-3" onSubmit={handleResearch}>
              <Input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Company domain or company name" />
              <Button type="submit" className="w-full bg-orange-500 text-white hover:bg-orange-400" disabled={loading || !isAuthenticated}>
                {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <ArrowRight className="mr-2 h-4 w-4" />}
                Launch research agent
              </Button>
            </form>
            <p className="mt-3 text-xs leading-5 text-slate-400">Trusted search, heuristic enrichment, ICP scoring, and outreach generation all run behind the API.</p>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-semibold text-white"><Sparkles className="h-4 w-4 text-orange-300" /> Status</div>
          </CardHeader>
          <CardBody>
            <p className="text-sm leading-6 text-slate-300">{message}</p>
            {profile ? (
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <div className="rounded-2xl border border-white/10 bg-black/20 p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Summary</div>
                  <div className="mt-2 text-sm text-white">{profile.insights.summary}</div>
                </div>
                <div className="rounded-2xl border border-white/10 bg-black/20 p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Signals</div>
                  <ul className="mt-2 space-y-2 text-sm text-slate-200">
                    {profile.insights.buying_signals.map((signal) => <li key={signal}>• {signal}</li>)}
                  </ul>
                </div>
              </div>
            ) : null}
          </CardBody>
        </Card>
      </section>

      {profile ? (
        <section className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <div className="text-sm font-semibold text-white">Company Profile</div>
            </CardHeader>
            <CardBody className="space-y-3 text-sm text-slate-300">
              <div><span className="text-slate-400">Name:</span> {profile.company.name}</div>
              <div><span className="text-slate-400">Domain:</span> {profile.company.domain}</div>
              <div><span className="text-slate-400">Industry:</span> {profile.company.industry}</div>
              <div><span className="text-slate-400">Description:</span> {profile.company.description}</div>
              <div><span className="text-slate-400">ICP score:</span> {profile.company.icp_score.toFixed(1)}</div>
              <div>
                <div className="text-slate-400">Executives</div>
                <div className="mt-2 space-y-2">
                  {profile.company.executives.map((executive) => (
                    <div key={executive.id} className="rounded-2xl border border-white/10 bg-black/20 p-3">
                      <div className="font-medium text-white">{executive.full_name}</div>
                      <div>{executive.title}</div>
                      {executive.linkedin_url ? <div className="truncate text-xs text-slate-400">{executive.linkedin_url}</div> : null}
                    </div>
                  ))}
                </div>
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              <div className="text-sm font-semibold text-white">Generated Outreach</div>
            </CardHeader>
            <CardBody className="space-y-4">
              {profile.company.drafts.map((draft) => (
                <div key={draft.id} className="rounded-3xl border border-white/10 bg-black/20 p-4">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <div className="text-sm font-medium text-white capitalize">{draft.kind.replaceAll('_', ' ')}</div>
                      <div className="text-xs uppercase tracking-[0.2em] text-slate-400">{draft.status} · {draft.crm_sync_status}</div>
                    </div>
                    <div className="flex gap-2">
                      <Button onClick={() => void approveDraft(draft.id)} className="border-orange-400/30 bg-orange-500/15 text-orange-100 hover:bg-orange-500/25">Approve</Button>
                      <Button onClick={() => void syncDraft(draft.id)}>Sync CRM</Button>
                    </div>
                  </div>
                  <div className="mt-3 text-sm text-slate-300">{draft.notes}</div>
                  <div className="mt-3 grid gap-2 text-xs text-slate-400">
                    {draft.subject_lines.map((line) => <div key={line} className="rounded-xl border border-white/10 bg-white/5 px-3 py-2">{line}</div>)}
                  </div>
                </div>
              ))}
            </CardBody>
          </Card>
        </section>
      ) : null}
    </main>
  );
}