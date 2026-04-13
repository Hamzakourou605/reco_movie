import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import { Film } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="navbar">
      <Link to="/" className="nav-brand">
        <Film size={28} color="#6366f1" />
        MyTflix
      </Link>
      
      <ul className="nav-links">
        <li>
          <NavLink 
            to="/" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
          >
            Accueil
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/top" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
          >
            Top Films
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/recommend" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
          >
            Pour Vous
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
