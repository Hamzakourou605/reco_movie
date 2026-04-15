import React, { useEffect, useState } from 'react';
import { getAdminStats } from '../api';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, Legend, LineChart, Line, AreaChart, Area
} from 'recharts';
import { 
  Users, Film, Star, Tag, TrendingUp, Loader2, 
  Activity, Award, ExternalLink, List, Terminal 
} from 'lucide-react';

const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f43f5e', '#f59e0b', '#10b981', '#06b6d4', '#3b82f6'];

const StatCard = ({ icon: Icon, label, value, color }) => (
  <div className="glass stat-card" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
    <div style={{ 
      background: `${color}15`, 
      padding: '0.6rem', 
      borderRadius: '10px', 
      color: color 
    }}>
      <Icon size={20} />
    </div>
    <div>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '0.1rem' }}>{label}</p>
      <h3 style={{ fontSize: '1.25rem', fontWeight: '700', margin: 0 }}>{value}</h3>
    </div>
  </div>
);

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getAdminStats();
        setStats(data);
      } catch (err) {
        console.error("Error fetching admin stats:", err);
        setError("Erreur lors du chargement des statistiques.");
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '10rem' }}>
      <Loader2 className="spinner" size={40} />
    </div>
  );

  if (error) return (
    <div className="glass fade-in" style={{ padding: '3rem', color: '#f87171', textAlign: 'center', margin: '2rem 0' }}>
      <p>{error}</p>
    </div>
  );

  return (
    <div className="admin-dashboard fade-in" style={{ marginTop: '2rem', paddingBottom: '4rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2.5rem' }}>
        <div style={{ background: 'var(--primary)', padding: '0.5rem', borderRadius: '8px' }}>
          <Activity size={24} color="#white" />
        </div>
        <div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: '800', margin: 0 }}>Espace Administration</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Vue d'ensemble et monitoring du système</p>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="stat-grid" style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', 
        gap: '1.25rem',
        marginBottom: '2.5rem'
      }}>
        <StatCard icon={Film} label="Total Films" value={stats.total_movies} color="#6366f1" />
        <StatCard icon={Users} label="Utilisateurs" value={stats.unique_users} color="#10b981" />
        <StatCard icon={Star} label="Évaluations" value={stats.total_ratings} color="#f59e0b" />
        <StatCard icon={Tag} label="Tags" value={stats.total_tags} color="#ec4899" />
        <StatCard icon={Award} label="Moyenne" value={stats.avg_rating} color="#3b82f6" />
      </div>

      {/* Activity Chart */}
      <div className="glass" style={{ padding: '2rem', marginBottom: '2.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: '600' }}>Activité Récente (30 jours)</h3>
          <span className="badge-live">Live</span>
        </div>
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={stats.activity_line}>
            <defs>
              <linearGradient id="colorRatings" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="var(--primary)" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis dataKey="date" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
            <YAxis stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
            <Tooltip 
              contentStyle={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
            />
            <Area type="monotone" dataKey="ratings" stroke="var(--primary)" strokeWidth={3} fillOpacity={1} fill="url(#colorRatings)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))', 
        gap: '2rem',
        marginBottom: '2.5rem'
      }}>
        {/* MLflow Runs */}
        <div className="glass" style={{ padding: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Terminal size={20} className="text-primary" /> Derniers Runs MLflow
            </h3>
            <a href={stats.mlflow_ui_url} target="_blank" rel="noopener noreferrer" className="btn-small">
              MLflow UI <ExternalLink size={14} />
            </a>
          </div>
          <div className="table-container">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>ID Run</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {stats.mlflow_runs.length > 0 ? stats.mlflow_runs.map((run, i) => (
                  <tr key={i}>
                    <td><code>{run.id}</code></td>
                    <td>{run.date}</td>
                    <td><span className={`status-pill ${run.status.toLowerCase()}`}>{run.status}</span></td>
                    <td style={{ fontWeight: '600', color: 'var(--primary)' }}>{run.accuracy}</td>
                  </tr>
                )) : (
                  <tr><td colSpan="4" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>Aucun run enregistré</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Best Rated Movies */}
        <div className="glass" style={{ padding: '2rem' }}>
          <h3 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Star size={20} color="#f59e0b" /> Best Rated (Min 10 votes)
          </h3>
          <div className="table-container">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Film</th>
                  <th>Note</th>
                  <th>Votes</th>
                </tr>
              </thead>
              <tbody>
                {stats.best_rated.map((movie, i) => (
                  <tr key={i}>
                    <td className="truncate-cell">{movie.name}</td>
                    <td><span style={{ color: '#fbbf24', fontWeight: 'bold' }}>{movie.value}</span></td>
                    <td>{movie.count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '2rem'
      }}>
        {/* Genre Distribution */}
        <div className="glass" style={{ padding: '2rem' }}>
          <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>Distribution par Genre</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats.genre_distribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={11} tickLine={false} />
              <YAxis stroke="var(--text-muted)" fontSize={11} tickLine={false} />
              <Tooltip 
                contentStyle={{ background: '#1e293b', border: 'none', borderRadius: '12px' }}
              />
              <Bar dataKey="value" fill="var(--primary)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Active Users */}
        <div className="glass" style={{ padding: '2rem' }}>
          <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>Utilisateurs les plus Actifs</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={stats.active_users}
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={90}
                paddingAngle={8}
                dataKey="value"
              >
                {stats.active_users.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend verticalAlign="bottom" height={36}/>
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
