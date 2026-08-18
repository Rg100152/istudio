#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
ISTUDIO - Interior Design & Architecture Website
A fully functional, production-ready, single-file Flask Application.
Targeted for 5000-6000 lines of robust, scalable code.
================================================================================
"""

import sqlite3
import json
import os
from flask import Flask, render_template_string, request, jsonify

# ==============================================================================
# 1. APPLICATION SETUP & CONFIGURATION
# ==============================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'istudio_secret_key_2026'
DATABASE = 'istudio.db'

# ==============================================================================
# 2. DATABASE LAYER (SQLITE HELPER FUNCTIONS)
# ==============================================================================
def get_db_connection():
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop tables if they exist to ensure a clean slate (optional, but good for seeding)
    cursor.execute("DROP TABLE IF EXISTS subscribers")
    cursor.execute("DROP TABLE IF EXISTS projects")
    cursor.execute("DROP TABLE IF EXISTS team")
    cursor.execute("DROP TABLE IF EXISTS testimonials")

    # Table: Projects
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
    ''')
    
    # Table: Team Members
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            bio TEXT NOT NULL,
            image_url TEXT NOT NULL,
            facebook TEXT,
            twitter TEXT,
            linkedin TEXT
        )
    ''')
    
    # Table: Testimonials
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS testimonials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            client_title TEXT NOT NULL,
            quote TEXT NOT NULL,
            rating INTEGER NOT NULL,
            image_url TEXT NOT NULL
        )
    ''')
    
    # Table: Newsletter Subscribers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[INFO] Database schema initialized successfully.")

def seed_db():
    """Seed the database with rich dummy data based on the wireframe requirement."""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("[INFO] Seeding database with rich data...")
    
    # 1. Seed Projects (6 Entries)
    projects_data = [
        ('Modern Loft Living Room', 'Living Room', 'A luxurious and modern open-concept living space with high ceilings and natural light.', 'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Minimalist Kitchen Renovation', 'Kitchen', 'Sleek white cabinetry combined with warm wood tones and smart storage solutions.', 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Corporate Office Interior', 'Commercial', 'A professional workspace designed for collaboration, featuring ergonomic furniture and breakout zones.', 'https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Cozy Bedroom Makeover', 'Bedroom', 'A tranquil and cozy bedroom suite designed with rich textures and a neutral color palette.', 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Artistic Home Office', 'Home Office', 'An inspiring home office that blends productivity with artistic decor and ergonomic design.', 'https://images.unsplash.com/photo-1593640408182-31c70c8268f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('Eco-Friendly Garden Studio', 'Outdoor', 'A sustainable garden studio with floor-to-ceiling glass walls, connecting the indoors with nature.', 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80')
    ]
    cursor.executemany('INSERT INTO projects (title, category, description, image_url) VALUES (?, ?, ?, ?)', projects_data)
    
    # 2. Seed Team Members (4 Entries)
    team_data = [
        ('Emily Thompson', 'Senior Interior Designer', 'With over 15 years of experience, Emily creates timeless spaces that reflect her clients\' personalities.', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', '#', '#', '#'),
        ('David Mitchell', 'Lead Architect', 'David specializes in innovative architectural solutions and sustainable building designs for modern living.', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', '#', '#', '#'),
        ('Sarah Johnson', 'Project Manager', 'Sarah ensures every project is delivered on time and within budget, coordinating seamlessly between teams.', 'https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', '#', '#', '#'),
        ('Michael Chen', 'Renovation Specialist', 'Michael brings life back to old buildings, transforming historical spaces into modern functional art.', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', '#', '#', '#')
    ]
    cursor.executemany('INSERT INTO team (name, title, bio, image_url, facebook, twitter, linkedin) VALUES (?, ?, ?, ?, ?, ?, ?)', team_data)
    
    # 3. Seed Testimonials (3 Entries)
    testimonials_data = [
        ('Robert Stevens', 'Homeowner', 'iSTUDIO completely transformed our outdated house into a modern masterpiece. The team understood our vision perfectly and exceeded our expectations.', 5, 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80'),
        ('Jessica Wong', 'Business Owner', 'We hired iSTUDIO for our corporate office renovation. The result is stunning and our employees love the new work environment. Highly recommend them!', 4, 'https://images.unsplash.com/photo-1494790100977-22676e3b9d35?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80'),
        ('David Bennett', 'Real Estate Developer', 'iSTUDIO is the best in the business. Their attention to detail, choice of materials, and innovative architectural approach sets them apart.', 5, 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&q=80')
    ]
    cursor.executemany('INSERT INTO testimonials (client_name, client_title, quote, rating, image_url) VALUES (?, ?, ?, ?, ?)', testimonials_data)
    
    conn.commit()
    conn.close()
    print("[INFO] Database seeding completed successfully.")

# ==============================================================================
# 3. DATA FETCH FUNCTIONS
# ==============================================================================
def get_all_projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return [dict(p) for p in projects]

def get_all_team():
    conn = get_db_connection()
    team = conn.execute('SELECT * FROM team').fetchall()
    conn.close()
    return [dict(t) for t in team]

def get_all_testimonials():
    conn = get_db_connection()
    testimonials = conn.execute('SELECT * FROM testimonials').fetchall()
    conn.close()
    return [dict(t) for t in testimonials]

# ==============================================================================
# 4. MASSIVE HTML TEMPLATE STRING (INCLUDING CSS & JS)
# ==============================================================================
TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iSTUDIO - Modern Interior Design & Architecture</title>
    <style>
        /* ====================================================================
               CSS RESET & GLOBAL STYLES
               ==================================================================== */
        *,
        *::before,
        *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: all 0.3s ease;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #FFFFFF;
            color: #333333;
            line-height: 1.6;
            overflow-x: hidden;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        ul {
            list-style: none;
        }

        img {
            max-width: 100%;
            display: block;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* ====================================================================
               TYPOGRAPHY & SECTION HEADERS
               ==================================================================== */
        h1,
        h2,
        h3,
        h4 {
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 15px;
        }

        h1 {
            font-size: 48px;
            color: #1a2b2c;
        }

        h2 {
            font-size: 36px;
            color: #005B5C;
        }

        h3 {
            font-size: 20px;
            color: #1a2b2c;
        }

        p {
            margin-bottom: 20px;
            color: #555;
            font-size: 16px;
        }

        .section-title {
            text-align: center;
            margin-bottom: 50px;
        }

        .section-title span {
            color: #005B5C;
        }

        .section-title p {
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #005B5C;
            font-weight: 600;
        }

        .section-title h2 {
            margin-top: 10px;
        }

        /* ====================================================================
               BUTTONS & UTILITY CLASSES
               ==================================================================== */
        .btn-primary {
            display: inline-block;
            padding: 12px 30px;
            background-color: #005B5C;
            color: #FFFFFF;
            border: 2px solid #005B5C;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            border-radius: 4px;
        }

        .btn-primary:hover {
            background-color: #004345;
            border-color: #004345;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 91, 92, 0.3);
        }

        .btn-secondary {
            display: inline-block;
            padding: 12px 30px;
            background-color: transparent;
            color: #005B5C;
            border: 2px solid #005B5C;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            border-radius: 4px;
        }

        .btn-secondary:hover {
            background-color: #005B5C;
            color: #FFFFFF;
            transform: translateY(-2px);
        }

        /* ====================================================================
               HEADER / NAVIGATION SECTION
               ==================================================================== */
        header {
            background-color: #FFFFFF;
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }

        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 28px;
            font-weight: 700;
            color: #1a2b2c;
            letter-spacing: -1px;
        }

        .logo span {
            color: #005B5C;
        }

        nav ul {
            display: flex;
            gap: 25px;
        }

        nav ul li a {
            font-size: 14px;
            font-weight: 600;
            color: #333333;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
        }

        nav ul li a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -5px;
            left: 0;
            background-color: #005B5C;
        }

        nav ul li a:hover::after {
            width: 100%;
        }

        nav ul li a:hover {
            color: #005B5C;
        }

        /* ====================================================================
               HERO SECTION
               ==================================================================== */
        .hero {
            padding: 80px 0;
            background: linear-gradient(to right, #FFFFFF 50%, #f4f7f6 50%);
        }

        .hero .container {
            display: flex;
            align-items: center;
            gap: 40px;
        }

        .hero-content {
            flex: 1;
        }

        .hero-content h1 {
            font-size: 54px;
            margin-bottom: 10px;
        }

        .hero-content h1 span {
            color: #005B5C;
        }

        .hero-content .subtitle {
            font-size: 18px;
            color: #005B5C;
            margin-bottom: 30px;
            font-weight: 500;
        }

        .hero-content p {
            font-size: 16px;
            margin-bottom: 30px;
            color: #666;
        }

        .hero-buttons {
            display: flex;
            gap: 15px;
            margin-bottom: 40px;
        }

        .hero-features {
            display: flex;
            gap: 30px;
        }

        .hero-features span {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 500;
            color: #333;
        }

        .hero-features span svg {
            fill: #005B5C;
            width: 20px;
            height: 20px;
        }

        .hero-image-grid {
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 200px 200px;
            gap: 15px;
            position: relative;
        }

        .hero-image-grid .img-box {
            background-color: #ddd;
            border-radius: 8px;
            overflow: hidden;
        }

        .hero-image-grid .img-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .hero-image-grid .img-box:nth-child(1) {
            grid-column: 1 / 3;
            grid-row: 1 / 2;
        }

        .hero-image-grid .img-box:nth-child(2) {
            grid-column: 1 / 2;
            grid-row: 2 / 3;
        }

        .hero-image-grid .img-box:nth-child(3) {
            grid-column: 2 / 3;
            grid-row: 2 / 3;
        }

        /* ====================================================================
               HISTORY / ABOUT SECTION
               ==================================================================== */
        .about {
            padding: 80px 0;
            background-color: #FFFFFF;
        }

        .about .container {
            display: flex;
            gap: 50px;
            align-items: center;
        }

        .about-grid {
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 180px 180px;
            gap: 15px;
        }

        .about-grid .img-box {
            background-color: #eee;
            border-radius: 8px;
            overflow: hidden;
        }

        .about-grid .img-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .about-grid .img-box:nth-child(1) {
            grid-column: 1 / 2;
            grid-row: 1 / 3;
            height: 375px;
        }

        .about-grid .img-box:nth-child(2) {
            grid-column: 2 / 3;
            grid-row: 1 / 2;
        }

        .about-grid .img-box:nth-child(3) {
            grid-column: 2 / 3;
            grid-row: 2 / 3;
        }

        .about-content {
            flex: 1;
        }

        .about-content h2 {
            margin-bottom: 20px;
        }

        .about-content h2 span {
            color: #005B5C;
        }

        .about-content p {
            color: #666;
            margin-bottom: 20px;
        }

        .about-counter {
            display: flex;
            gap: 40px;
            margin-top: 30px;
        }

        .counter-item {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .counter-item .num {
            font-size: 32px;
            font-weight: 700;
            color: #005B5C;
        }

        .counter-item .label {
            font-size: 14px;
            color: #555;
            font-weight: 500;
        }

        .counter-item .label span {
            display: block;
            font-weight: 400;
            font-size: 12px;
            color: #888;
        }

        /* ====================================================================
               WHY CHOOSE US SECTION
               ==================================================================== */
        .features {
            padding: 80px 0;
            background-color: #f9f9f9;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
        }

        .feature-card {
            background: #FFFFFF;
            padding: 30px 20px;
            text-align: center;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        }

        .feature-card .icon-box {
            width: 70px;
            height: 70px;
            background-color: #e8f2f2;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
        }

        .feature-card .icon-box svg {
            width: 30px;
            height: 30px;
            fill: #005B5C;
        }

        .feature-card h4 {
            margin-bottom: 10px;
            color: #1a2b2c;
        }

        .feature-card p {
            font-size: 14px;
            color: #777;
            margin-bottom: 0;
        }

        /* ====================================================================
               LATEST PROJECTS SECTION (FILTERABLE)
               ==================================================================== */
        .projects {
            padding: 80px 0;
            background-color: #FFFFFF;
        }

        .projects-filter {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 40px;
        }

        .projects-filter button {
            background: none;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 600;
            color: #555;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.3s ease;
        }

        .projects-filter button:hover,
        .projects-filter button.active {
            background-color: #005B5C;
            color: #FFFFFF;
        }

        .projects-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
        }

        .project-card {
            background: #f9f9f9;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease;
        }

        .project-card:hover {
            transform: scale(1.03);
        }

        .project-card .img-box {
            height: 200px;
            overflow: hidden;
        }

        .project-card .img-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .project-card .project-info {
            padding: 20px;
        }

        .project-card .project-info h4 {
            font-size: 18px;
            margin-bottom: 5px;
        }

        .project-card .project-info p {
            font-size: 14px;
            color: #777;
            margin-bottom: 0;
        }

        /* ====================================================================
               OUR CREATIVE SERVICES SECTION
               ==================================================================== */
        .services {
            padding: 80px 0;
            background-color: #f4f7f6;
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
        }

        .service-card {
            background: #FFFFFF;
            padding: 30px 20px;
            border-radius: 8px;
            text-align: center;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
        }

        .service-card:hover {
            border-bottom-color: #005B5C;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        }

        .service-card h4 {
            font-size: 18px;
            margin-bottom: 10px;
        }

        .service-card p {
            font-size: 14px;
            color: #666;
            margin-bottom: 0;
        }

        .service-card .service-icon {
            margin-bottom: 15px;
        }

        .service-card .service-icon svg {
            width: 40px;
            height: 40px;
            fill: #005B5C;
        }

        /* ====================================================================
               OUR PROFESSIONAL DESIGNERS SECTION
               ==================================================================== */
        .designers {
            padding: 80px 0;
            background-color: #FFFFFF;
        }

        .designers-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
        }

        .designer-card {
            background: #f9f9f9;
            border-radius: 8px;
            padding: 30px 20px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .designer-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            background: #FFFFFF;
        }

        .designer-card .img-box {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            overflow: hidden;
            margin: 0 auto 20px;
            border: 4px solid #e8f2f2;
        }

        .designer-card .img-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .designer-card h4 {
            margin-bottom: 5px;
            color: #1a2b2c;
        }

        .designer-card span {
            font-size: 14px;
            color: #005B5C;
            font-weight: 500;
        }

        .designer-card p {
            font-size: 13px;
            color: #777;
            margin-top: 10px;
        }

        .designer-card .social-links {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 15px;
        }

        .designer-card .social-links a svg {
            width: 18px;
            height: 18px;
            fill: #888;
            transition: fill 0.3s ease;
        }

        .designer-card .social-links a:hover svg {
            fill: #005B5C;
        }

        /* ====================================================================
               TESTIMONIALS / CUSTOMER CAROUSEL SECTION
               ==================================================================== */
        .testimonials {
            padding: 80px 0;
            background-color: #f4f7f6;
        }

        .testimonial-carousel {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            overflow: hidden;
        }

        .testimonial-item {
            background: #FFFFFF;
            padding: 40px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
            display: none;
            animation: fadeIn 0.8s ease;
        }

        .testimonial-item.active {
            display: block;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .testimonial-item .client-img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            overflow: hidden;
            margin: 0 auto 20px;
        }

        .testimonial-item .client-img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .testimonial-item .quote {
            font-size: 18px;
            font-style: italic;
            color: #555;
            margin-bottom: 20px;
        }

        .testimonial-item .client-name {
            font-weight: 700;
            color: #1a2b2c;
            margin-bottom: 5px;
        }

        .testimonial-item .client-title {
            font-size: 14px;
            color: #888;
        }

        .testimonial-item .rating {
            margin-bottom: 15px;
        }

        .testimonial-item .rating svg {
            width: 18px;
            height: 18px;
            fill: #FFD700;
        }

        .carousel-controls {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }

        .carousel-controls button {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 2px solid #005B5C;
            background: transparent;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }

        .carousel-controls button:hover {
            background: #005B5C;
        }

        .carousel-controls button svg {
            width: 20px;
            height: 20px;
            fill: #005B5C;
        }

        .carousel-controls button:hover svg {
            fill: #FFFFFF;
        }

        /* ====================================================================
               NEWSLETTER & FOOTER SECTION
               ==================================================================== */
        .newsletter {
            padding: 60px 0;
            background-color: #005B5C;
            text-align: center;
        }

        .newsletter h2 {
            color: #FFFFFF;
            margin-bottom: 10px;
        }

        .newsletter p {
            color: #e0ecec;
            margin-bottom: 30px;
        }

        .newsletter-form {
            display: flex;
            justify-content: center;
            gap: 15px;
            max-width: 500px;
            margin: 0 auto;
        }

        .newsletter-form input[type="email"] {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            outline: none;
        }

        .newsletter-form button {
            padding: 15px 30px;
            background-color: #FFFFFF;
            color: #005B5C;
            border: none;
            border-radius: 4px;
            font-weight: 700;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .newsletter-form button:hover {
            background-color: #e8f2f2;
        }

        .newsletter-form .msg-success {
            color: #d4edda;
            margin-top: 15px;
            font-size: 14px;
            display: none;
        }

        .newsletter-form .msg-error {
            color: #f8d7da;
            margin-top: 15px;
            font-size: 14px;
            display: none;
        }

        footer {
            background-color: #1a2b2c;
            color: #b0c4c4;
            padding: 60px 0 30px;
        }

        footer .container {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 40px;
            margin-bottom: 40px;
        }

        footer h4 {
            color: #FFFFFF;
            font-size: 18px;
            margin-bottom: 20px;
        }

        footer p {
            font-size: 14px;
            color: #b0c4c4;
        }

        footer ul li {
            margin-bottom: 10px;
        }

        footer ul li a {
            font-size: 14px;
            color: #b0c4c4;
            transition: color 0.3s ease;
        }

        footer ul li a:hover {
            color: #FFFFFF;
        }

        footer .footer-bottom {
            border-top: 1px solid #2c4041;
            padding-top: 20px;
            text-align: center;
            font-size: 14px;
            color: #889c9c;
        }

        /* ====================================================================
               RESPONSIVE MEDIA QUERIES
               ==================================================================== */
        @media screen and (max-width: 992px) {
            .hero .container {
                flex-direction: column;
            }
            .hero {
                background: #FFFFFF;
            }
            .about .container {
                flex-direction: column;
            }
            .services-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .designers-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            footer .container {
                grid-template-columns: repeat(2, 1fr);
            }
            .projects-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media screen and (max-width: 768px) {
            header .container {
                flex-direction: column;
                gap: 15px;
            }
            nav ul {
                flex-wrap: wrap;
                justify-content: center;
            }
            h1 {
                font-size: 32px;
            }
            .hero-content h1 {
                font-size: 36px;
            }
            .hero-image-grid {
                grid-template-columns: 1fr;
                grid-template-rows: auto;
            }
            .hero-image-grid .img-box:nth-child(1),
            .hero-image-grid .img-box:nth-child(2),
            .hero-image-grid .img-box:nth-child(3) {
                grid-column: 1 / 2;
                height: 200px;
            }
            .about-grid {
                grid-template-columns: 1fr;
            }
            .about-grid .img-box:nth-child(1),
            .about-grid .img-box:nth-child(2),
            .about-grid .img-box:nth-child(3) {
                grid-column: 1 / 2;
                height: 200px;
            }
            .features-grid {
                grid-template-columns: 1fr 1fr;
            }
            .projects-grid {
                grid-template-columns: 1fr;
            }
            .services-grid {
                grid-template-columns: 1fr;
            }
            .designers-grid {
                grid-template-columns: 1fr;
            }
            footer .container {
                grid-template-columns: 1fr;
                text-align: center;
            }
            .newsletter-form {
                flex-direction: column;
                padding: 0 20px;
            }
            .about-counter {
                flex-direction: column;
            }
        }

        @media screen and (max-width: 480px) {
            .features-grid {
                grid-template-columns: 1fr;
            }
            .hero-features {
                flex-direction: column;
                gap: 10px;
            }
        }
        /* End CSS */
    </style>
</head>
<body>

    <!-- ================================================================
    HEADER & NAVIGATION
    ================================================================ -->
    <header>
        <div class="container">
            <div class="logo">i<span>STUDIO</span></div>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#services">Services</a></li>
                    <li><a href="#projects">Projects</a></li>
                    <li><a href="#designers">Designers</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- ================================================================
    HERO SECTION
    ================================================================ -->
    <section class="hero" id="home">
        <div class="container">
            <div class="hero-content">
                <h1>We Make Your <span>Home Better</span></h1>
                <div class="subtitle">An Award Winning Studio Since 1990</div>
                <p>We are a premier interior design and architecture firm dedicated to transforming spaces into functional, aesthetic, and inspirational environments. Our team blends creativity with technical expertise to deliver exceptional results tailored to your unique lifestyle.</p>
                <div class="hero-buttons">
                    <a href="#projects" class="btn-primary">View Our Work</a>
                    <a href="#contact" class="btn-secondary">Contact Us</a>
                </div>
                <div class="hero-features">
                    <span>
                        <!-- SVG Icon: Furniture -->
                        <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 18H4V4h16v16z"/><path d="M9 10h6v4H9z"/></svg>
                        Crafted Furniture
                    </span>
                    <span>
                        <!-- SVG Icon: Leaf -->
                        <svg viewBox="0 0 24 24"><path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66l.95-2.3c.48.17.98.3 1.5.3c2.88 0 5.05-2.13 6.19-4.9c1.06-2.58 1.51-5.29 2.65-8.1z"/><path d="M21 3c-1.11 0-2 .89-2 2h-2c0-1.11-.89-2-2-2H5v2h14v14c0 1.11.89 2 2 2z"/></svg>
                        Sustainable Material
                    </span>
                    <span>
                        <!-- SVG Icon: Star -->
                        <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21z"/></svg>
                        Innovative Architects
                    </span>
                    <span>
                        <!-- SVG Icon: Dollar -->
                        <svg viewBox="0 0 24 24"><path d="M11.5 2v2.06c-2.6.32-4.5 1.77-4.5 3.94c0 2.17 1.9 3.62 4.5 3.94v4.06c-1.32-.13-2.24-.63-2.84-1.38l-1.75 1.12C8.07 17.1 9.7 18.07 11.5 18.06V20h1v-1.94c2.6-.32 4.5-1.77 4.5-3.94c0-2.17-1.9-3.62-4.5-3.94V6.06c1.32.13 2.24.63 2.84 1.38l1.75-1.12C15.93 4.9 14.3 3.93 12.5 3.94V2h-1zm0 8.06c-1.23-.15-2.04-.58-2.04-1.29c0-.71.81-1.14 2.04-1.29v2.58zm1 1.88v2.58c1.23-.15 2.04-.58 2.04-1.29c0-.71-.81-1.14-2.04-1.29z"/></svg>
                        Budget Friendly
                    </span>
                </div>
            </div>
            <div class="hero-image-grid">
                <div class="img-box"><img src="https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Modern Interior Design"></div>
                <div class="img-box"><img src="https://images.unsplash.com/photo-1550581190-9c1c48d21d6c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Living Room Design"></div>
                <div class="img-box"><img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Kitchen Design"></div>
            </div>
        </div>
    </section>

    <!-- ================================================================
    HISTORY / ABOUT SECTION
    ================================================================ -->
    <section class="about" id="about">
        <div class="container">
            <div class="about-grid">
                <div class="img-box"><img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="About Studio"></div>
                <div class="img-box"><img src="https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Architecture Detail"></div>
                <div class="img-box"><img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Design Process"></div>
            </div>
            <div class="about-content">
                <h2><span>HISTORY</span> of Our Creation</h2>
                <p>Founded in 1990, iSTUDIO has grown from a small architectural practice into one of the most respected interior design firms in the region. Our journey is defined by a relentless pursuit of innovation, craftsmanship, and client satisfaction. We believe that great design has the power to enhance lives, boost productivity, and create a deep sense of belonging.</p>
                <p>Our philosophy is centered on collaboration, sustainability, and timeless aesthetics. Whether it's a residential renovation, a commercial overhaul, or a new architectural project, we approach every challenge with fresh eyes and a dedication to excellence.</p>
                <div class="about-counter">
                    <div class="counter-item">
                        <span class="num">25+</span>
                        <span class="label">Years Of <span>Experience</span></span>
                    </div>
                    <div class="counter-item">
                        <span class="num">120+</span>
                        <span class="label">Awards <span>Won</span></span>
                    </div>
                    <div class="counter-item">
                        <span class="num">99%</span>
                        <span class="label">Client <span>Satisfaction</span></span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- ================================================================
    WHY CHOOSE US (FEATURES) SECTION
    ================================================================ -->
    <section class="features">
        <div class="container">
            <div class="section-title">
                <p>Why People</p>
                <h2>CHOOSE US</h2>
            </div>
            <div class="features-grid">
                <!-- Feature 1 -->
                <div class="feature-card">
                    <div class="icon-box">
                        <svg viewBox="0 0 24 24"><path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11z"/></svg>
                    </div>
                    <h4>25+ Years Experience</h4>
                    <p>With over a quarter-century of dedicated service, we bring unparalleled expertise, industry insights, and proven design strategies to every single project we undertake, ensuring excellence from start to finish.</p>
                </div>
                <!-- Feature 2 -->
                <div class="feature-card">
                    <div class="icon-box">
                        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                    </div>
                    <h4>Best Interior Design</h4>
                    <p>We curate spaces that seamlessly blend functionality with artistic vision. Our award-winning designs are customized to reflect your personality while optimizing the architectural potential of your space.</p>
                </div>
                <!-- Feature 3 -->
                <div class="feature-card">
                    <div class="icon-box">
                        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
                    </div>
                    <h4>Innovative Architects</h4>
                    <p>Pushing the boundaries of traditional architecture, we integrate smart technology, sustainable materials, and avant-garde structural concepts to create futuristic yet practical living environments.</p>
                </div>
                <!-- Feature 4 -->
                <div class="feature-card">
                    <div class="icon-box">
                        <svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                    </div>
                    <h4>Customer Satisfaction</h4>
                    <p>Our clients are at the heart of everything we do. We maintain transparent communication, uphold strict quality standards, and go above and beyond to ensure your dream home becomes a tangible reality.</p>
                </div>
                <!-- Feature 5 -->
                <div class="feature-card">
                    <div class="icon-box">
                        <svg viewBox="0 0 24 24"><path d="M11.5 2v2.06c-2.6.32-4.5 1.77-4.5 3.94c0 2.17 1.9 3.62 4.5 3.94v4.06c-1.32-.13-2.24-.63-2.84-1.38l-1.75 1.12C8.07 17.1 9.7 18.07 11.5 18.06V20h1v-1.94c2.6-.32 4.5-1.77 4.5-3.94c0-2.17-1.9-3.62-4.5-3.94V6.06c1.32.13 2.24.63 2.84 1.38l1.75-1.12C15.93 4.9 14.3 3.93 12.5 3.94V2h-1zm0 8.06c-1.23-.15-2.04-.58-2.04-1.29c0-.71.81-1.14 2.04-1.29v2.58zm1 1.88v2.58c1.23-.15 2.04-.58 2.04-1.29c0-.71-.81-1.14-2.04-1.29z"/></svg>
                    </div>
                    <h4>Budget Friendly</h4>
                    <p>We believe exceptional design should be accessible. Through smart resource allocation, strategic planning, and cost-effective material sourcing, we deliver premium results that respect your financial boundaries.</p>
                </div>
                <!-- Feature 6 -->
                <div class="feature-card">
                    <div class="icon-box">
                        <svg viewBox="0 0 24 24"><path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66l.95-2.3c.48.17.98.3 1.5.3c2.88 0 5.05-2.13 6.19-4.9c1.06-2.58 1.51-5.29 2.65-8.1z"/><path d="M21 3c-1.11 0-2 .89-2 2h-2c0-1.11-.89-2-2-2H5v2h14v14c0 1.11.89 2 2 2z"/></svg>
                    </div>
                    <h4>Sustainable Material</h4>
                    <p>We are committed to protecting the planet. Our designs prioritize eco-friendly materials, energy-efficient solutions, and sustainable building practices that reduce environmental impact without compromising on style.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- ================================================================
    LATEST PROJECTS SECTION
    ================================================================ -->
    <section class="projects" id="projects">
        <div class="container">
            <div class="section-title">
                <p>Our Latest</p>
                <h2>PROJECTS</h2>
            </div>
            <div class="projects-filter">
                <button class="active" data-filter="all">All</button>
                <button data-filter="Living Room">Living Room</button>
                <button data-filter="Kitchen">Kitchen</button>
                <button data-filter="Commercial">Commercial</button>
                <button data-filter="Bedroom">Bedroom</button>
                <button data-filter="Outdoor">Outdoor</button>
            </div>
            <div class="projects-grid" id="projectsGrid">
                {% for project in projects %}
                <div class="project-card" data-category="{{ project.category }}">
                    <div class="img-box">
                        <img src="{{ project.image_url }}" alt="{{ project.title }}">
                    </div>
                    <div class="project-info">
                        <h4>{{ project.title }}</h4>
                        <p>{{ project.category }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- ================================================================
    OUR CREATIVE SERVICES SECTION
    ================================================================ -->
    <section class="services" id="services">
        <div class="container">
            <div class="section-title">
                <p>Our Creative</p>
                <h2>SERVICES</h2>
            </div>
            <div class="services-grid">
                <!-- Service 1 -->
                <div class="service-card">
                    <div class="service-icon">
                        <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                    </div>
                    <h4>Interior Design</h4>
                    <p>Our interior design service transforms residential and commercial spaces into beautiful, functional environments. From color palettes to furniture selection, we handle every detail to ensure a cohesive and inspiring aesthetic.</p>
                </div>
                <!-- Service 2 -->
                <div class="service-card">
                    <div class="service-icon">
                        <svg viewBox="0 0 24 24"><path d="M17 4h-3V2h-4v2H7c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2z"/></svg>
                    </div>
                    <h4>Renovation</h4>
                    <p>Breathing new life into old structures is our passion. We handle complete home and office renovations, including structural changes, modernizing fixtures, and updating the overall character of the property to meet contemporary standards.</p>
                </div>
                <!-- Service 3 -->
                <div class="service-card">
                    <div class="service-icon">
                        <svg viewBox="0 0 24 24"><path d="M21 2H3c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM3 4h18v2H3V4zm0 4h18v6H3V8z"/></svg>
                    </div>
                    <h4>Commercial</h4>
                    <p>We specialize in designing high-performance commercial spaces, including offices, retail stores, and hospitality venues. Our commercial designs focus on branding, traffic flow, employee well-being, and maximizing operational efficiency.</p>
                </div>
                <!-- Service 4 -->
                <div class="service-card">
                    <div class="service-icon">
                        <svg viewBox="0 0 24 24"><path d="M19 2h-4v2h4v16h-4v2h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/><path d="M9 2H5c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
                    </div>
                    <h4>Implementation</h4>
                    <p>Our comprehensive implementation service covers project management, procurement, construction oversight, and final installation. We ensure that your design vision is executed flawlessly, on schedule, and within the allocated budget.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- ================================================================
    OUR PROFESSIONAL DESIGNERS SECTION
    ================================================================ -->
    <section class="designers" id="designers">
        <div class="container">
            <div class="section-title">
                <p>Our Professional</p>
                <h2>DESIGNERS</h2>
            </div>
            <div class="designers-grid">
                {% for member in team %}
                <div class="designer-card">
                    <div class="img-box">
                        <img src="{{ member.image_url }}" alt="{{ member.name }}">
                    </div>
                    <h4>{{ member.name }}</h4>
                    <span>{{ member.title }}</span>
                    <p>{{ member.bio }}</p>
                    <div class="social-links">
                        <a href="{{ member.facebook }}"><svg viewBox="0 0 24 24"><path d="M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm13 2h-2.5A3.5 3.5 0 0 0 12 8.5V11h-2v3h2v7h3v-7h3v-3h-3V9a1 1 0 0 1 1-1h2V5z"/></svg></a>
                        <a href="{{ member.twitter }}"><svg viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"/></svg></a>
                        <a href="{{ member.linkedin }}"><svg viewBox="0 0 24 24"><path d="M4.98 3.5c0 1.38-1.12 2.5-2.5 2.5S0 4.88 0 3.5 1.12 1 2.48 1s2.5 1.12 2.5 2.5zM.5 5h4v14h-4V5zM20.5 9.5c0-3-1.8-4.5-4.5-4.5-1.6 0-2.8.7-3.5 1.7V5h-4v14h4v-9c0-1 .5-2 2-2s2 1 2 2v9h4v-9.5z"/></svg></a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- ================================================================
    TESTIMONIALS SECTION (JAVASCRIPT SLIDER)
    ================================================================ -->
    <section class="testimonials" id="contact">
        <div class="container">
            <div class="section-title">
                <p>Customer</p>
                <h2>SATISFACTION</h2>
            </div>
            <div class="testimonial-carousel">
                {% for testimonial in testimonials %}
                <div class="testimonial-item {% if loop.first %}active{% endif %}">
                    <div class="client-img">
                        <img src="{{ testimonial.image_url }}" alt="{{ testimonial.client_name }}">
                    </div>
                    <div class="rating">
                        {% for _ in range(testimonial.rating) %}
                        <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21z"/></svg>
                        {% endfor %}
                    </div>
                    <div class="quote">"{{ testimonial.quote }}"</div>
                    <div class="client-name">{{ testimonial.client_name }}</div>
                    <div class="client-title">{{ testimonial.client_title }}</div>
                </div>
                {% endfor %}
            </div>
            <div class="carousel-controls">
                <button id="prevBtn">
                    <svg viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
                </button>
                <button id="nextBtn">
                    <svg viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
                </button>
            </div>
        </div>
    </section>

    <!-- ================================================================
    NEWSLETTER & FOOTER SECTION
    ================================================================ -->
    <section class="newsletter">
        <div class="container">
            <h2>Subscribe the NEWSLETTER</h2>
            <p>Stay updated with our latest design trends, project showcases, and exclusive offers.</p>
            <form class="newsletter-form" id="newsletterForm">
                <input type="email" placeholder="Enter your email address" required>
                <button type="submit">Subscribe</button>
            </form>
            <div id="newsletterMsgSuccess" class="msg-success">Thank you for subscribing! You will receive our updates shortly.</div>
            <div id="newsletterMsgError" class="msg-error">An error occurred. Please try again later.</div>
        </div>
    </section>

    <footer>
        <div class="container">
            <div>
                <h4>iSTUDIO</h4>
                <p>iSTUDIO is a leading interior design and architecture firm dedicated to transforming spaces into works of art. With a rich history dating back to 1990, we continue to innovate and inspire through our comprehensive design solutions.</p>
            </div>
            <div>
                <h4>Quick Links</h4>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About Us</a></li>
                    <li><a href="#services">Our Services</a></li>
                    <li><a href="#projects">Recent Projects</a></li>
                    <li><a href="#designers">Our Team</a></li>
                </ul>
            </div>
            <div>
                <h4>Services</h4>
                <ul>
                    <li><a href="#">Interior Design</a></li>
                    <li><a href="#">Renovation</a></li>
                    <li><a href="#">Commercial Design</a></li>
                    <li><a href="#">Implementation</a></li>
                    <li><a href="#">Consultation</a></li>
                </ul>
            </div>
            <div>
                <h4>Contact Info</h4>
                <ul>
                    <li>123 Design Avenue, New York, NY 10001</li>
                    <li>Phone: +1 (212) 555-1234</li>
                    <li>Email: info@istudio.com</li>
                    <li>Working Hours: Mon - Fri, 9:00 AM - 6:00 PM</li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="container">
                &copy; 2026 iSTUDIO. All Rights Reserved. Designed with passion for extraordinary living.
            </div>
        </div>
    </footer>

    <!-- ================================================================
    JAVASCRIPT LOGIC (FILTERING, SLIDER, AJAX)
    ================================================================ -->
    <script>
        (function() {
            "use strict";

            // -----------------------------------------------------------------
            // 1. PROJECTS FILTERING
            // -----------------------------------------------------------------
            const filterButtons = document.querySelectorAll('.projects-filter button');
            const projectCards = document.querySelectorAll('.project-card');

            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    // Remove active class from all buttons
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    // Add active class to clicked button
                    this.classList.add('active');

                    const filterValue = this.getAttribute('data-filter');
                    projectCards.forEach(card => {
                        const category = card.getAttribute('data-category');
                        if (filterValue === 'all' || category === filterValue) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                });
            });

            // -----------------------------------------------------------------
            // 2. TESTIMONIAL CAROUSEL
            // -----------------------------------------------------------------
            const testimonialItems = document.querySelectorAll('.testimonial-item');
            let currentTestimonial = 0;
            const totalTestimonials = testimonialItems.length;

            function showTestimonial(index) {
                testimonialItems.forEach(item => item.classList.remove('active'));
                testimonialItems[index].classList.add('active');
            }

            document.getElementById('nextBtn').addEventListener('click', function() {
                currentTestimonial = (currentTestimonial + 1) % totalTestimonials;
                showTestimonial(currentTestimonial);
            });

            document.getElementById('prevBtn').addEventListener('click', function() {
                currentTestimonial = (currentTestimonial - 1 + totalTestimonials) % totalTestimonials;
                showTestimonial(currentTestimonial);
            });

            // Auto-play carousel every 6 seconds
            setInterval(() => {
                currentTestimonial = (currentTestimonial + 1) % totalTestimonials;
                showTestimonial(currentTestimonial);
            }, 6000);

            // -----------------------------------------------------------------
            // 3. NEWSLETTER AJAX SUBMISSION
            // -----------------------------------------------------------------
            const newsletterForm = document.getElementById('newsletterForm');
            const msgSuccess = document.getElementById('newsletterMsgSuccess');
            const msgError = document.getElementById('newsletterMsgError');

            newsletterForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const emailInput = this.querySelector('input[type="email"]');
                const email = emailInput.value.trim();

                // Basic validation
                if (!email || !email.includes('@')) {
                    alert('Please enter a valid email address.');
                    return;
                }

                const formData = new FormData();
                formData.append('email', email);

                fetch('/api/subscribe', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        msgSuccess.style.display = 'block';
                        msgError.style.display = 'none';
                        emailInput.value = '';
                        setTimeout(() => { msgSuccess.style.display = 'none'; }, 5000);
                    } else {
                        msgError.style.display = 'block';
                        msgSuccess.style.display = 'none';
                        setTimeout(() => { msgError.style.display = 'none'; }, 5000);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    msgError.style.display = 'block';
                    msgSuccess.style.display = 'none';
                    setTimeout(() => { msgError.style.display = 'none'; }, 5000);
                });
            });

        })();
    </script>
</body>
</html>
"""

# ==============================================================================
# 5. ROUTES & CONTROLLERS
# ==============================================================================
@app.route('/')
def index():
    """Render the main homepage with dynamic data from the database."""
    try:
        projects = get_all_projects()
        team = get_all_team()
        testimonials = get_all_testimonials()
    except Exception as e:
        print(f"[ERROR] Failed to fetch data: {e}")
        projects, team, testimonials = [], [], []
    
    return render_template_string(
        TEMPLATE_HTML,
        projects=projects,
        team=team,
        testimonials=testimonials
    )

@app.route('/api/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Handle AJAX newsletter subscription request."""
    email = request.form.get('email')
    if not email or '@' not in email:
        return jsonify({'success': False, 'message': 'Invalid email address.'})
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Subscription successful.'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'This email is already subscribed.'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Internal server error.'})

# ==============================================================================
# 6. MAIN EXECUTION BLOCK
# ==============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("           iSTUDIO - Architecture & Interior Design")
    print("                     Production Server")
    print("=" * 60)
    
    # Initialize and seed the database if it doesn't exist or on first run
    if not os.path.exists(DATABASE):
        print("[INFO] Database not found. Initializing and seeding...")
        init_db()
        seed_db()
    else:
        print("[INFO] Database found. Checking schema consistency...")
        # Re-run init to ensure new tables are created if missing, 
        # but skip seeding to prevent duplicates. 
        # In production, migrations handle this, for this monolithic script we just check integrity.
        try:
            conn = sqlite3.connect(DATABASE)
            conn.execute('SELECT 1 FROM projects LIMIT 1')
            conn.close()
        except sqlite3.OperationalError:
            print("[WARNING] Existing database schema outdated. Re-creating and seeding...")
            os.remove(DATABASE)
            init_db()
            seed_db()
            
    print("[INFO] Starting Flask development server...")
    print("[INFO] Access the website at: http://127.0.0.1:5000")
    print("[INFO] Press CTRL+C to stop the server.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)