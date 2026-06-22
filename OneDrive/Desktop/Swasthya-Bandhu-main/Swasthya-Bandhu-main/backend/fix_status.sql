-- Fix appointment statuses from 'confirmed' to 'scheduled'
-- Run this in your MySQL database

UPDATE appointments SET status = 'scheduled' WHERE status = 'confirmed';

-- Verify the change
SELECT id, user_id, doctor_id, date, time, status FROM appointments;
