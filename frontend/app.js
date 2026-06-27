const authSection = document.getElementById('auth-section');
const appSection = document.getElementById('app-section');
const applicationsList = document.getElementById('applications-list');
const applicationDetailCard = document.getElementById('application-detail-card');
const messageBox = document.getElementById('message');

const tokenKey = 'jobCopilotToken';
let selectedApplicationId = null;

function showMessage(text, type = 'info') {
  messageBox.textContent = text;
  messageBox.className = `message ${type}`;
  messageBox.classList.remove('hidden');
  setTimeout(() => messageBox.classList.add('hidden'), 4000);
}

function getAuthHeader() {
  const token = localStorage.getItem(tokenKey);
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let json = null;
  try { json = JSON.parse(text); } catch (err) {}
  if (!response.ok) {
    throw new Error(json?.detail || text || 'Request failed');
  }
  return json ?? text;
}

async function login(event) {
  event.preventDefault();
  const usernameInput = document.getElementById('login-username');
  const passwordInput = document.getElementById('login-password');
  const username = usernameInput.value.trim();
  const password = passwordInput.value;
  
  if (!username || !password) {
    showMessage('Please enter both username and password', 'error');
    return;
  }
  
  try {
    const data = await requestJson('/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username, password }),
    });
    localStorage.setItem(tokenKey, data.access_token);
    
    // Clear form fields
    usernameInput.value = '';
    passwordInput.value = '';
    
    showMessage('Login successful!', 'info');
    showApp();
  } catch (err) {
    showMessage(err.message || 'Login failed. Please check your credentials.', 'error');
  }
}

async function signup(event) {
  event.preventDefault();
  const usernameInput = document.getElementById('signup-username');
  const passwordInput = document.getElementById('signup-password');
  const username = usernameInput.value.trim();
  const password = passwordInput.value;
  
  if (!username || !password) {
    showMessage('Please enter both username and password', 'error');
    return;
  }
  
  if (password.length < 4) {
    showMessage('Password must be at least 4 characters', 'error');
    return;
  }
  
  try {
    const data = await requestJson('/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    localStorage.setItem(tokenKey, data.access_token);
    
    // Clear form fields
    usernameInput.value = '';
    passwordInput.value = '';
    
    showMessage(`Welcome ${username}! Account created successfully.`, 'info');
    showApp();
  } catch (err) {
    showMessage(err.message || 'Signup failed. Username might already exist.', 'error');
  }
}

function logout() {
  localStorage.removeItem(tokenKey);
  selectedApplicationId = null;
  
  // Clear all form fields
  const forms = document.querySelectorAll('form');
  forms.forEach(form => form.reset());
  
  // Clear file selection
  if (typeof clearFileSelection === 'function') {
    clearFileSelection();
  }
  
  authSection.classList.remove('hidden');
  appSection.classList.add('hidden');
  applicationDetailCard.classList.add('hidden');
  
  showMessage('Logged out successfully', 'info');
}

async function showApp() {
  authSection.classList.add('hidden');
  appSection.classList.remove('hidden');
  await loadApplications();
}

async function createApplication(event) {
  event.preventDefault();
  const form = document.getElementById('application-form');
  const formData = new FormData();
  formData.append('job_title', document.getElementById('job-title').value);
  formData.append('company', document.getElementById('company').value);
  formData.append('jd_text', document.getElementById('jd-text').value);
  formData.append('jd_url', document.getElementById('jd-url').value);
  const file = document.getElementById('resume-file').files[0];
  if (!file) {
    showMessage('Please upload a PDF resume.', 'error');
    return;
  }
  formData.append('resume_file', file);

  // Show loading overlay
  showLoadingOverlay();
  
  try {
    await requestJson('/applications', {
      method: 'POST',
      headers: getAuthHeader(),
      body: formData,
    });
    
    hideLoadingOverlay();
    showMessage('Application created successfully! 🎉', 'info');
    form.reset();
    clearFileSelection();
    await loadApplications();
  } catch (err) {
    hideLoadingOverlay();
    showMessage(err.message || 'Failed to create application. Please try again.', 'error');
  }
}

function showLoadingOverlay() {
  const overlay = document.getElementById('loading-overlay');
  const submitBtn = document.getElementById('submit-application-btn');
  
  overlay.classList.remove('hidden');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Creating...';
  submitBtn.style.opacity = '0.6';
  
  // Animate steps
  let stepIndex = 0;
  const steps = ['step-1', 'step-2', 'step-3', 'step-4'];
  
  const animateStep = () => {
    if (stepIndex < steps.length) {
      const step = document.getElementById(steps[stepIndex]);
      const icon = step.querySelector('.step-icon');
      
      // Mark current step as active
      step.classList.add('active');
      icon.textContent = '⚡';
      
      stepIndex++;
      
      // Continue animation every 5 seconds
      if (stepIndex < steps.length) {
        setTimeout(animateStep, 5000);
      }
    }
  };
  
  // Start animation after 1 second
  setTimeout(animateStep, 1000);
  
  // Store interval ID so we can clear it
  window.loadingAnimationStarted = true;
}

function hideLoadingOverlay() {
  const overlay = document.getElementById('loading-overlay');
  const submitBtn = document.getElementById('submit-application-btn');
  
  overlay.classList.add('hidden');
  submitBtn.disabled = false;
  submitBtn.textContent = 'Generate Application';
  submitBtn.style.opacity = '1';
  
  // Reset all steps
  const steps = document.querySelectorAll('.loading-step');
  steps.forEach(step => {
    step.classList.remove('active');
    const icon = step.querySelector('.step-icon');
    icon.textContent = '⏳';
  });
  
  window.loadingAnimationStarted = false;
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    document.getElementById('file-name').textContent = file.name;
    document.getElementById('file-selected').classList.remove('hidden');
    document.getElementById('file-label').classList.add('file-has-selection');
  }
}

function clearFileSelection() {
  document.getElementById('resume-file').value = '';
  document.getElementById('file-selected').classList.add('hidden');
  document.getElementById('file-label').classList.remove('file-has-selection');
  document.getElementById('file-name').textContent = '';
}

async function loadApplications() {
  try {
    const items = await requestJson('/applications', {
      headers: { ...getAuthHeader(), 'Content-Type': 'application/json' },
    });
    applicationsList.innerHTML = items.length ? items.map(renderApplicationCard).join('') : '<p>No applications yet.</p>';
  } catch (err) {
    showMessage(err.message, 'error');
  }
}

function renderApplicationCard(app) {
  return `
    <div class="application-card">
      <div>
        <strong>${app.job_title}</strong> at ${app.company}
        <div class="small-text">Status: ${app.status}</div>
      </div>
      <button onclick="viewApplication(${app.id})">View</button>
    </div>
  `;
}

async function viewApplication(id) {
  selectedApplicationId = id;
  try {
    const app = await requestJson(`/applications/${id}`, {
      headers: { ...getAuthHeader(), 'Content-Type': 'application/json' },
    });
    document.getElementById('detail-heading').textContent = `${app.job_title} at ${app.company}`;
    document.getElementById('detail-status').textContent = app.status;
    document.getElementById('status-select').value = app.status;
    document.getElementById('original-resume').innerHTML = renderDiffText(app.original_resume_text || 'No resume text available.', app.drafts?.resume_rewrite || 'No rewritten resume available.', true);
    document.getElementById('rewritten-resume').innerHTML = renderDiffText(app.original_resume_text || 'No resume text available.', app.drafts?.resume_rewrite || 'No rewritten resume available.', false);
    document.getElementById('ats-score').textContent = app.drafts?.ats_score || 'No ATS score available.';
    document.getElementById('fit-analysis').textContent = app.drafts?.fit_analysis || 'No fit analysis available.';
    document.getElementById('cover-letter').textContent = app.drafts?.cover_letter || 'No cover letter available.';
    document.getElementById('interview-qa').textContent = app.drafts?.interview_qa || 'No interview questions available.';
    applicationDetailCard.classList.remove('hidden');
    document.getElementById('applications-card').scrollIntoView({ behavior: 'smooth' });
  } catch (err) {
    showMessage(err.message, 'error');
  }
}

async function updateStatus() {
  if (!selectedApplicationId) return;
  try {
    const status = document.getElementById('status-select').value;
    await requestJson(`/applications/${selectedApplicationId}/status`, {
      method: 'PUT',
      headers: { ...getAuthHeader(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    document.getElementById('detail-status').textContent = status;
    showMessage('Status updated.');
    await loadApplications();
  } catch (err) {
    showMessage(err.message, 'error');
  }
}

async function regenerateSection(section) {
  if (!selectedApplicationId) return;
  try {
    let url = `/applications/${selectedApplicationId}/regenerate`;
    let method = 'PUT';
    let options = {
      method,
      headers: { ...getAuthHeader(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ section }),
    };

    if (section === 'ats_score') {
      url = `/applications/${selectedApplicationId}/ats-score`;
      options = {
        method: 'POST',
        headers: getAuthHeader(),
      };
    }

    await requestJson(url, options);
    showMessage(section === 'ats_score' ? 'ATS score computed.' : `Regenerated ${section.replace('_', ' ')}.`);
    await viewApplication(selectedApplicationId);
  } catch (err) {
    showMessage(err.message, 'error');
  }
}

function escapeHtml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderDiffText(originalText, rewrittenText, isOriginal) {
  const originalLines = originalText.split(/\r?\n/);
  const rewrittenLines = rewrittenText.split(/\r?\n/);
  const maxLines = Math.max(originalLines.length, rewrittenLines.length);
  let html = '';

  for (let i = 0; i < maxLines; i += 1) {
    const originalLine = originalLines[i] || '';
    const rewrittenLine = rewrittenLines[i] || '';
    const same = originalLine.trim() === rewrittenLine.trim();

    if (isOriginal) {
      html += `<div class="line ${same ? '' : 'diff-old'}">${escapeHtml(originalLine || '')}</div>`;
    } else {
      html += `<div class="line ${same ? '' : 'diff-new'}">${escapeHtml(rewrittenLine || '')}</div>`;
    }
  }
  return html;
}

async function downloadArtifact(url, filename) {
  try {
    const response = await fetch(url, {
      headers: getAuthHeader(),
    });
    if (!response.ok) {
      const text = await response.text();
      throw new Error(text || 'Download failed');
    }
    const blob = await response.blob();
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  } catch (err) {
    showMessage(err.message, 'error');
  }
}

function setupEventListeners() {
  document.getElementById('login-form').addEventListener('submit', login);
  document.getElementById('signup-form').addEventListener('submit', signup);
  document.getElementById('logout-btn').addEventListener('click', logout);
  document.getElementById('application-form').addEventListener('submit', createApplication);
  document.getElementById('resume-file').addEventListener('change', handleFileSelect);
  document.getElementById('clear-file').addEventListener('click', clearFileSelection);
  document.getElementById('save-status').addEventListener('click', updateStatus);
  document.getElementById('back-list').addEventListener('click', () => {
    applicationDetailCard.classList.add('hidden');
  });
  document.querySelectorAll('[data-section]').forEach((button) => {
    button.addEventListener('click', () => regenerateSection(button.dataset.section));
  });
  document.getElementById('download-cover').addEventListener('click', () => {
    downloadArtifact(`/applications/${selectedApplicationId}/download/cover-letter`, 'cover_letter.docx');
  });
  document.getElementById('download-resume').addEventListener('click', () => {
    downloadArtifact(`/applications/${selectedApplicationId}/download/resume`, 'resume.pdf');
  });
}

function initialize() {
  setupEventListeners();
  
  // Ensure loading overlay is hidden on page load
  const loadingOverlay = document.getElementById('loading-overlay');
  if (loadingOverlay) {
    loadingOverlay.classList.add('hidden');
  }
  
  if (localStorage.getItem(tokenKey)) {
    showApp();
  }
}

initialize();
