// ===== GLOBAL STATE =====
let currentUser = null;
let courseBlocks = [];
let currentEditingCourseId = null;
let currentEditingSimulatorBlockId = null;
let simulatorCache = [];
let authToken = localStorage.getItem("token") || null;
let myCourses = [];
let availableCourses = [];
let allUsers = [];
let courseQuestions = [];
let currentEditingQuestionId = null;
let lastDeletedQuestion = null; // Store last deleted question for undo

// Global keyboard listener for Ctrl+Z undo
document.addEventListener('keydown', async (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'z' && lastDeletedQuestion) {
    e.preventDefault();
    console.log('⏪ Ctrl+Z pressed - Undoing quiz deletion');

    if (!currentEditingCourseId) {
      console.warn('Cannot undo: no course being edited');
      return;
    }

    // Re-create the question via API
    try {
      const response = await fetch(`http://localhost:3000/api/courses/${currentEditingCourseId}/questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(lastDeletedQuestion)
      });

      const result = await response.json();
      if (result.success) {
        alert('✅ Question restored!');
        await loadCourseQuestions(currentEditingCourseId);

        // Clear all placeholders and re-render
        const editor = document.getElementById('course-content-editor');
        editor.querySelectorAll('.quiz-question-placeholder').forEach(p => p.remove());
        courseQuestions.forEach(q => insertQuizPlaceholder(q.question_text, q.id));

        lastDeletedQuestion = null; // Clear undo history
      } else {
        alert('Error restoring question: ' + result.message);
      }
    } catch (error) {
      console.error('Error undoing deletion:', error);
      alert('Error restoring question');
    }
  }
});


// ===== INITIALIZATION =====
document.addEventListener("DOMContentLoaded", () => {
  initializeApp();
});

function initializeApp() {
  setupAuthListeners();
  setupNavigationListeners();
  setupCourseEditorListeners();
  setupMessageListeners();
  setupQuizModalListeners();

  if (authToken) {
    fetchUserProfile();
  } else {
    showAuthSection();
  }
}

function setupMessageListeners() {
  window.addEventListener("message", (e) => {
    if (e.data.type === "closeBlockSimulator") {
      showDashboard();
    }
  });
}

// ===== AUTHENTICATION =====
function setupAuthListeners() {
  const loginForm = document.querySelector("#login-form form");
  const registerForm = document.querySelector("#register-form form");
  const logoutButton = document.getElementById("logout-button");
  const showRegister = document.getElementById("show-register");
  const showLogin = document.getElementById("show-login");

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      handleLogin();
    });
  }

  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault();
      handleRegister();
    });
  }

  if (logoutButton) {
    logoutButton.addEventListener("click", handleLogout);
  }

  if (showRegister) {
    showRegister.addEventListener("click", (e) => {
      e.preventDefault();
      document.getElementById("login-form").style.display = "none";
      document.getElementById("register-form").style.display = "block";
    });
  }

  if (showLogin) {
    showLogin.addEventListener("click", (e) => {
      e.preventDefault();
      document.getElementById("login-form").style.display = "block";
      document.getElementById("register-form").style.display = "none";
    });
  }
}

function handleLogin() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;
  const errorMessage = document.getElementById("login-error-message");

  if (!email || !password) {
    errorMessage.textContent = "Please fill in all fields";
    return;
  }

  fetch("http://localhost:3000/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        authToken = data.data.token;
        localStorage.setItem("token", authToken);
        // Backend returns: {token, user: {id, email, role, shells}}
        const userData = data.data.user || data.data;
        currentUser = {
          id: userData.id,
          email: userData.email,
          role: userData.role,
          shells: userData.shells || 0
        };
        console.log("Login successful, currentUser set:", currentUser);
        // INSTANT: Show dashboard immediately without needing a reload
        showDashboard();
        // Also load initial data in background
        setTimeout(() => {
          if (currentUser?.role === "superadmin") {
            loadAllUsers();
            loadPendingCourses();
            loadUserCourses();
            loadAvailableCourses();
          } else if (currentUser?.role === "admin") {
            loadPendingCourses();
            loadUserCourses();
            loadAvailableCourses();
          } else {
            loadUserCourses();
            loadAvailableCourses();
          }
        }, 0);
      } else {
        errorMessage.textContent = data.message || "Login failed";
      }
    })
    .catch((err) => {
      console.error("Login error:", err);
      errorMessage.textContent =
        "Connection error. Backend running on port 3000?";
    });
}

function handleRegister() {
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;
  const errorMessage = document.getElementById("register-error-message");

  if (!email || !password) {
    errorMessage.textContent = "Please fill in all fields";
    return;
  }

  fetch("http://localhost:3000/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        errorMessage.style.color = "green";
        errorMessage.textContent =
          "Registration successful! You can now login.";
        setTimeout(() => {
          document.getElementById("register-form").style.display = "none";
          document.getElementById("login-form").style.display = "block";
        }, 1500);
      } else {
        errorMessage.textContent = data.message || "Registration failed";
      }
    })
    .catch((err) => {
      console.error("Register error:", err);
      errorMessage.textContent = "Connection error. Backend running?";
    });
}

function fetchUserProfile() {
  fetch("http://localhost:3000/api/users/profile", {
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        currentUser = data.data;
        showDashboard();
      } else {
        logout();
      }
    })
    .catch((err) => {
      console.error("Profile fetch error:", err);
      logout();
    });
}

function handleLogout() {
  logout();
}

function logout() {
  console.log("LOGOUT CALLED - Token will be cleared!");
  console.warn("⚠️ Clearing token from localStorage");
  authToken = null;
  currentUser = null;
  localStorage.removeItem("token");
  console.log("Token cleared from localStorage");
  showAuthSection();
}

// ===== TOKEN VALIDATION =====
/**
 * Validate and check if token is still valid
 */
function validateAuthToken() {
  const token = localStorage.getItem("token");
  if (!token) {
    console.warn("⚠️ No token found in localStorage");
    return false;
  }

  // Check token format (JWT has 3 parts)
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      console.error("Invalid token format - expected 3 parts, got", parts.length);
      return false;
    }

    // Decode payload
    const payload = JSON.parse(atob(parts[1]));
    const expiryTime = payload.exp * 1000;

    if (Date.now() > expiryTime) {
      console.warn("⚠️ Token expired at:", new Date(expiryTime).toISOString());
      return false;
    }

    console.log("✓ Token is valid, expires at:", new Date(expiryTime).toISOString());
    return true;
  } catch (e) {
    console.error("❌ Invalid token format:", e.message);
    return false;
  }
}

// ===== TOKEN MONITORING =====
// Monitor localStorage changes and warn if token is cleared unexpectedly
if (typeof window !== 'undefined') {
  setInterval(() => {
    const currentToken = localStorage.getItem("token");
    if (!currentToken && authToken) {
      console.warn("⚠️ WARNING: Token was cleared from localStorage but authToken still exists!");
      console.log("This may indicate an unexpected logout or session clear");
    }
  }, 2000);
}

// ===== NAVIGATION =====
function setupNavigationListeners() {
  const dashboardLink = document.getElementById("dashboard-link");
  const homeLink = document.getElementById("home-link");

  if (dashboardLink) {
    dashboardLink.addEventListener("click", (e) => {
      e.preventDefault();
      showDashboard();
    });
  }

  if (homeLink) {
    homeLink.addEventListener("click", (e) => {
      e.preventDefault();
      if (currentUser) {
        showDashboard();
      } else {
        showAuthSection();
      }
    });
  }
}

// ===== COURSE EDITOR LISTENERS =====
function setupCourseEditorListeners() {
  const courseForm = document.getElementById("course-form");
  const cancelBtn = document.getElementById("cancel-course-edit");
  const backBtn = document.getElementById("back-to-dashboard");
  const saveDraftBtn = document.getElementById("save-draft-btn");
  const submitApprovalBtn = document.getElementById("submit-approval-btn");

  // Save draft button - DIRECTLY call saveCourse with "draft" action
  if (saveDraftBtn) {
    saveDraftBtn.addEventListener("click", (e) => {
      e.preventDefault();
      console.log("📝 Save Draft button clicked - action: draft");
      saveCourse("draft");
    });
  }

  // Submit for approval button - DIRECTLY call saveCourse with "pending" action
  if (submitApprovalBtn) {
    submitApprovalBtn.addEventListener("click", (e) => {
      e.preventDefault();
      console.log("📝 Submit for Approval button clicked - action: pending");
      saveCourse("pending");
    });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener("click", showDashboard);
  }

  if (backBtn) {
    backBtn.addEventListener("click", showDashboard);
  }

  // Rich text editor toolbar
  setupRichTextEditor();
}

function setupRichTextEditor() {
  const buttons = document.querySelectorAll(".editor-toolbar button");
  const contentEditor = document.getElementById("course-content-editor");

  buttons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const command = button.dataset.command;
      const id = button.id;

      if (id === "insert-math-simulator") {
        showMarketplaceSelector("math");
      } else if (id === "insert-coding-simulator") {
        showMarketplaceSelector("coding");
      } else if (id === "insert-visual-simulator") {
        addVisualSimulator();
      } else if (id === "insert-block-simulator") {
        addBlockSimulator();
      } else {
        document.execCommand(command, false, null);
        contentEditor.focus();
      }
    });
  });
}

function showMarketplaceSelector(type) {
  // Fetch marketplace simulators
  fetch(`http://localhost:3000/api/simulators?limit=50`, {
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        showSimulatorSelectionModal(data.data.simulators, type);
      }
    })
    .catch((err) => console.error("Error loading simulators:", err));
}

function showSimulatorSelectionModal(simulators, type) {
  const html = `
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999;">
            <div style="background: white; padding: 20px; border-radius: 8px; max-width: 600px; max-height: 80vh; overflow-y: auto;">
                <h3>Select a Simulator</h3>
                <div id="simulator-list" style="margin: 20px 0;">
                    ${simulators
      .map(
        (sim) => `
                        <div style="padding: 10px; border: 1px solid #ddd; margin: 10px 0; border-radius: 4px; cursor: pointer;" onclick="selectSimulatorForCourse(${sim.id
          }, '${type}', '${sim.title.replace(/'/g, "\\'")}')">
                            <strong>${sim.title}</strong>
                            <p style="margin: 5px 0; font-size: 0.9em; color: #666;">${sim.description || "No description"
          }</p>
                            <p style="margin: 5px 0; font-size: 0.8em; color: #999;">by ${sim.creator_email
          } | Downloads: ${sim.downloads}</p>
                        </div>
                    `
      )
      .join("")}
                </div>
                <button onclick="closeSimulatorModal()" style="padding: 8px 16px; background: #999; color: white; border: none; border-radius: 4px; cursor: pointer;">Close</button>
            </div>
        </div>
    `;
  document.body.insertAdjacentHTML("beforeend", html);
}

function selectSimulatorForCourse(simulatorId, type, title) {
  const blockId = Date.now();
  courseBlocks.push({
    id: blockId,
    type: `${type}-simulator`,
    title: title,
    simulatorId: simulatorId,
    data: { simulatorId: simulatorId },
  });

  insertSimulatorBlock(
    blockId,
    title,
    `${type.charAt(0).toUpperCase() + type.slice(1)} Simulator`
  );
  closeSimulatorModal();
}

function closeSimulatorModal() {
  const modal = document.querySelector('[style*="position: fixed"]');
  if (modal) modal.remove();
}

function addVisualSimulator() {
  const blockId = Date.now();
  courseBlocks.push({
    id: blockId,
    type: "visual-simulator",
    title: "Code-based Visual Simulator",
    data: { code: "", variables: {} },
  });

  insertSimulatorBlock(blockId, "Code-based Visual", "Code-based Simulator");
}

function addBlockSimulator() {
  const blockId = Date.now();
  courseBlocks.push({
    id: blockId,
    type: "block-simulator",
    title: "Block-based Simulator",
    data: { blocks: [], connections: [] },
  });

  insertSimulatorBlock(
    blockId,
    "Block-based Simulator",
    "Block-based Simulator"
  );
}

function insertSimulatorBlock(blockId, title, type) {
  const contentEditor = document.getElementById("course-content-editor");
  const simulatorDiv = document.createElement("div");
  simulatorDiv.className = "simulator-block";
  simulatorDiv.dataset.blockId = blockId;
  simulatorDiv.style.cssText =
    "background: #f0f0f0; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; border-radius: 4px;";
  simulatorDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>${type}</strong>
                <p style="margin: 5px 0; color: #666;">${title}</p>
            </div>
            <div style="display: flex; gap: 10px;">
                <button type="button" onclick="handleEditSimulator(event, ${blockId})" style="padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">Edit</button>
                <button type="button" onclick="handleRemoveSimulator(event, ${blockId})" style="padding: 5px 10px; background: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;">Remove</button>
            </div>
        </div>
    `;
  contentEditor.appendChild(simulatorDiv);
}

// ===== UI RENDERING =====
function showAuthSection() {
  document.getElementById("auth-section").style.display = "block";
  document.getElementById("dashboard-section").style.display = "none";
  document.getElementById("course-editor-section").style.display = "none";
  document.getElementById("course-viewer-section").style.display = "none";

  document.getElementById("simulator-link").style.display = "none";
  document.getElementById("marketplace-link").style.display = "none";
  document.getElementById("creator-link").style.display = "none";
  document.getElementById("dashboard-link").style.display = "none";
  document.getElementById("logout-button").style.display = "none";

  document.getElementById("login-link").style.display = "inline";
  document.getElementById("register-link").style.display = "inline";
}

function showDashboard() {
  document.getElementById("auth-section").style.display = "none";
  document.getElementById("dashboard-section").style.display = "block";
  document.getElementById("course-editor-section").style.display = "none";
  document.getElementById("course-viewer-section").style.display = "none";

  document.getElementById("simulator-link").style.display = "inline";
  document.getElementById("marketplace-link").style.display = "inline";
  document.getElementById("creator-link").style.display = "inline";
  document.getElementById("dashboard-link").style.display = "inline";
  document.getElementById("logout-button").style.display = "inline";

  document.getElementById("login-link").style.display = "none";
  document.getElementById("register-link").style.display = "none";

  document.getElementById("user-email").textContent =
    currentUser?.email || "User";

  // INSTANT: Show dashboard content immediately
  if (currentUser?.role === "superadmin") {
    showSuperadminDashboard();
  } else if (currentUser?.role === "admin") {
    showAdminDashboard();
  } else {
    showUserDashboard();
  }

  // INSTANT: Load all data asynchronously in background without blocking UI
  setTimeout(() => {
    if (currentUser?.role === "superadmin") {
      loadAllUsers();
      loadPendingCourses();
      loadUserCourses();
      loadAvailableCourses();
    } else if (currentUser?.role === "admin") {
      loadPendingCourses();
      loadUserCourses();
      loadAvailableCourses();
    } else {
      loadUserCourses();
      loadAvailableCourses();
    }
  }, 0);
}

function showSuperadminDashboard() {
  document.getElementById("user-dashboard").style.display = "none";
  document.getElementById("admin-dashboard").style.display = "none";
  document.getElementById("superadmin-dashboard").style.display = "block";

  // INSTANT: Only set up event listeners, data loads in showDashboard() asynchronously
  document
    .getElementById("create-course-button-superadmin")
    ?.addEventListener("click", createNewCourse);
}

function showAdminDashboard() {
  document.getElementById("user-dashboard").style.display = "none";
  document.getElementById("superadmin-dashboard").style.display = "none";
  document.getElementById("admin-dashboard").style.display = "block";

  // INSTANT: Only set up event listeners, data loads in showDashboard() asynchronously
  document
    .getElementById("create-course-button-admin")
    ?.addEventListener("click", createNewCourse);
}

function showUserDashboard() {
  document.getElementById("superadmin-dashboard").style.display = "none";
  document.getElementById("admin-dashboard").style.display = "none";
  document.getElementById("user-dashboard").style.display = "block";

  // INSTANT: Only set up event listeners, data loads in showDashboard() asynchronously
  document
    .getElementById("create-course-button-user")
    ?.addEventListener("click", createNewCourse);
}

function loadAllUsers() {
  fetch("http://localhost:3000/api/users", {
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        allUsers = data.data;
        renderUserList();
      } else {
        console.error("Error loading users:", data.message);
      }
    })
    .catch((err) => console.error("Error loading users:", err));
}

function renderUserList() {
  const userList = document.getElementById("user-list");
  if (!userList) return;

  userList.innerHTML = allUsers
    .map(
      (user) => `
        <li>
            <strong>${user.email}</strong>
            <p>Role: ${user.role} | Shells: ${user.shells}</p>
            <button onclick="changeUserRole('${user.email}', 'admin')">Make Admin</button>
            <button onclick="changeUserRole('${user.email}', 'teacher')">Make Teacher</button>
            <button onclick="changeUserRole('${user.email}', 'user')">Make User</button>
        </li>
    `
    )
    .join("");
}

function changeUserRole(email, newRole) {
  fetch(`http://localhost:3000/api/admin/users/${email}/role`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${authToken}`,
    },
    body: JSON.stringify({ role: newRole }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert(`User role changed to ${newRole}`);
        loadAllUsers();
      } else {
        alert("Error: " + data.message);
      }
    })
    .catch((err) => console.error("Error changing role:", err));
}

function loadPendingCourses() {
  fetch("http://localhost:3000/api/admin/courses/pending", {
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        renderPendingCourses(data.data);
      }
    })
    .catch((err) => console.error("Error loading pending courses:", err));
}

function renderPendingCourses(courses) {
  const list =
    document.getElementById("superadmin-pending-courses-list") ||
    document.getElementById("admin-pending-courses-list");
  if (!list) return;

  if (courses.length === 0) {
    list.innerHTML = "<li><em>No pending courses</em></li>";
    return;
  }

  list.innerHTML = courses
    .map(
      (course) => `
        <li>
            <strong>${course.title}</strong>
            <p>${course.description || "No description"}</p>
            <button onclick="previewCourse(${course.id})">Preview</button>
            <button onclick="approveCourse(${course.id})">Approve</button>
            <button onclick="rejectCourse(${course.id})">Reject</button>
        </li>
    `
    )
    .join("");
}

function previewCourse(courseId) {
  viewCourse(courseId);
}

function approveCourse(courseId) {
  fetch(`http://localhost:3000/api/admin/courses/${courseId}/status`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${authToken}`,
    },
    body: JSON.stringify({ status: "approved" }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("Course approved!");
        loadPendingCourses();
        loadAvailableCourses();
      }
    })
    .catch((err) => console.error("Error approving course:", err));
}

function rejectCourse(courseId) {
  fetch(`http://localhost:3000/api/admin/courses/${courseId}/status`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${authToken}`,
    },
    body: JSON.stringify({ status: "rejected" }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("Course rejected!");
        loadPendingCourses();
      }
    })
    .catch((err) => console.error("Error rejecting course:", err));
}

function loadUserCourses() {
  console.log("=== LOADING USER COURSES ===");
  fetch("http://localhost:3000/api/courses", {
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        const allCoursesFromServer = data.data || [];
        console.log("Total courses from API:", allCoursesFromServer.length);
        console.log("Current user ID:", currentUser.id);

        myCourses = allCoursesFromServer.filter(
          (c) => c.creator_id === currentUser.id
        );
        console.log("Filtered user courses:", myCourses.length);
        renderUserCourses();
      }
    })
    .catch((err) => console.error("Error loading user courses:", err));
}

function loadAvailableCourses() {
  console.log("=== LOADING AVAILABLE COURSES ===");
  fetch("http://localhost:3000/api/courses", {
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        const allCoursesFromServer = data.data || [];
        console.log("Total courses from API:", allCoursesFromServer.length);
        console.log(
          "Course statuses:",
          allCoursesFromServer.map((c) => ({
            id: c.id,
            title: c.title,
            status: c.status,
            creator_id: c.user_id,
            currentUserId: currentUser.id,
          }))
        );

        availableCourses = allCoursesFromServer.filter(
          (c) => c.status === "approved" && c.creator_id !== currentUser.id
        );
        console.log("Filtered available courses:", availableCourses.length);
        renderAvailableCourses();
      }
    })
    .catch((err) => console.error("Error loading available courses:", err));
}

function renderUserCourses() {
  const lists = [
    document.getElementById("my-courses-list-user"),
    document.getElementById("my-courses-list-admin"),
    document.getElementById("my-courses-list-superadmin"),
  ];

  lists.forEach((list) => {
    if (!list) return;

    // INSTANT: Clear existing list to prevent duplicates
    list.innerHTML = "";

    if (myCourses.length === 0) {
      list.innerHTML = "<li><em>No courses yet</em></li>";
      return;
    }

    // INSTANT: Build and append items one by one instead of replacing all
    myCourses.forEach((course) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${course.title}</strong>
        <p>${course.description || "No description"}</p>
        <span style="background: ${course.status === "pending" ? "#ff9800" : "#4caf50"
        }; color: white; padding: 4px 8px; border-radius: 3px; font-size: 0.9em;">
            ${course.status?.toUpperCase() || "UNKNOWN"}
        </span>
        <button onclick="editCourse(${course.id})">Edit</button>
        <button onclick="viewCourse(${course.id})">View</button>
        <button onclick="deleteCourse(${course.id})">Delete</button>
      `;
      list.appendChild(li);
    });
  });
}

function renderAvailableCourses() {
  const lists = [
    document.getElementById("available-courses-list-user"),
    document.getElementById("available-courses-list-admin"),
    document.getElementById("available-courses-list-superadmin"),
  ];

  lists.forEach((list) => {
    if (!list) return;

    // INSTANT: Clear existing list to prevent duplicates
    list.innerHTML = "";

    if (availableCourses.length === 0) {
      list.innerHTML = "<li><em>No available courses</em></li>";
      return;
    }

    // INSTANT: Build and append items one by one instead of replacing all
    availableCourses.forEach((course) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${course.title}</strong>
        <p>${course.description || "No description"}</p>
        <button onclick="viewCourse(${course.id})">View</button>
        <button onclick="enrollInCourse(${course.id})">Enroll</button>
      `;
      list.appendChild(li);
    });
  });
}

function createNewCourse() {
  currentEditingCourseId = null;
  courseBlocks = [];
  document.getElementById("course-title").value = "";
  document.getElementById("course-description").value = "";
  document.getElementById("course-content-editor").innerHTML = "";

  document.getElementById("dashboard-section").style.display = "none";
  document.getElementById("course-editor-section").style.display = "block";
}

function editCourse(courseId) {
  currentEditingCourseId = courseId;
  const course = myCourses.find((c) => c.id === courseId);

  if (course) {
    document.getElementById("course-title").value = course.title;
    document.getElementById("course-description").value =
      course.description || "";
    document.getElementById("course-content-editor").innerHTML =
      course.content || "";

    // RESTORE SAVED BLOCKS from the course
    courseBlocks = course.blocks ?
      (typeof course.blocks === 'string' ? JSON.parse(course.blocks) : course.blocks)
      : [];

    console.log("✓ Course loaded with", courseBlocks.length, "blocks");
    console.log("  Blocks:", courseBlocks);

    // Load quiz questions for this course and re-render placeholders
    loadCourseQuestions(courseId).then(() => {
      // IMPORTANT: Clear all existing placeholders first to prevent duplicates
      const editor = document.getElementById('course-content-editor');
      const existingPlaceholders = editor.querySelectorAll('.quiz-question-placeholder');
      existingPlaceholders.forEach(p => p.remove());

      // Re-render quiz placeholders in the editor
      courseQuestions.forEach(q => {
        insertQuizPlaceholder(q.question_text, q.id);
      });
    });

    document.getElementById("dashboard-section").style.display = "none";
    document.getElementById("course-editor-section").style.display = "block";
  }
}

function saveCourse(action = "draft") {
  const title = document.getElementById("course-title").value;
  const description = document.getElementById("course-description").value;
  const contentEditor = document.getElementById("course-content-editor");

  // Clone the editor content and remove quiz placeholders before saving
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = contentEditor.innerHTML;
  const quizPlaceholders = tempDiv.querySelectorAll('.quiz-question-placeholder');
  quizPlaceholders.forEach(p => p.remove());
  const content = tempDiv.innerHTML;

  if (!title.trim()) {
    alert("Please enter a course title");
    return;
  }

  // Set course status based on action
  const status = action === "pending" ? "pending" : "draft";

  console.log(`\n=== SAVE COURSE DEBUG ===`);
  console.log(`Action: ${action}`);
  console.log(`Status to save: ${status}`);
  console.log(`Title: "${title}"`);
  console.log(`Description: "${description}"`);
  console.log(`Content HTML length: ${content.length}`);
  console.log(`courseBlocks count: ${courseBlocks.length}`);
  console.log(`courseBlocks:`, courseBlocks);

  const url = currentEditingCourseId
    ? `http://localhost:3000/api/courses/${currentEditingCourseId}`
    : "http://localhost:3000/api/courses";

  const method = currentEditingCourseId ? "PUT" : "POST";

  const courseData = {
    title: title,
    description: description,
    content: content,
    status: status,
    blocks: JSON.stringify(courseBlocks),
  };

  console.log(`Sending ${method} request to ${url}`);
  console.log(`Payload:`, courseData);

  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${authToken}`,
    },
    body: JSON.stringify(courseData),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(`Response:`, data);
      if (data.success) {
        // Set currentEditingCourseId if this was a new course
        if (!currentEditingCourseId) {
          currentEditingCourseId = data.data?.id || data.data;
          console.log("✅ New course saved, currentEditingCourseId set to:", currentEditingCourseId);
        }

        const message =
          action === "pending"
            ? "Course submitted for approval!"
            : "Course saved as draft!";
        alert(message);

        // INSTANT: Stay in editor, just reload course data in background
        loadUserCourses();
        if (action === "pending") {
          loadPendingCourses();
        }

        // DON'T navigate away - stay in editor for seamless quiz editing
        // showDashboard(); // REMOVED - user wants to stay in editor
      } else {
        alert(`Error: ${data.message || "Failed to save course"}`);
      }
    })
    .catch((err) => {
      console.error("Error saving course:", err);
      alert("Error saving course. Check console for details.");
    });
}

function viewCourse(courseId) {
  const course = myCourses.find((c) => c.id === courseId) ||
    availableCourses.find((c) => c.id === courseId);

  if (!course) {
    alert("Course not found");
    return;
  }

  document.getElementById("dashboard-section").style.display = "none";
  document.getElementById("course-editor-section").style.display = "none";
  document.getElementById("course-viewer-section").style.display = "block";

  const viewerContent = document.getElementById("course-viewer-content");
  viewerContent.innerHTML = `
        <h1>${course.title}</h1>
        <p><strong>Description:</strong> ${course.description || "No description"}</p>
        <div id="course-content-display" style="margin: 20px 0;">
            ${course.content || "No content"}
        </div>
        <button onclick="showDashboard()" style="padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">Back</button>
    `;

  // Set currentEditingCourseId for quiz answer submission
  currentEditingCourseId = courseId;

  // Load and display course simulators
  loadCourseSimulators(courseId);

  // Load and render quiz questions
  renderQuizQuestionsInViewer(courseId);

  // Convert Edit buttons to Run buttons for course simulators
  convertSimulatorButtonsForViewer(courseId, course);
}

function convertSimulatorButtonsForViewer(courseId, course) {
  // Load courseBlocks from the course
  courseBlocks = course.blocks ?
    (typeof course.blocks === 'string' ? JSON.parse(course.blocks) : course.blocks)
    : [];

  // Find all simulator blocks in the viewer
  const simulatorDivs = document.querySelectorAll('.simulator-block');
  simulatorDivs.forEach((div) => {
    const blockId = parseInt(div.dataset.blockId);
    const buttons = div.querySelectorAll('button');

    // Replace Edit/Remove buttons with Run button
    buttons.forEach((btn) => {
      if (btn.textContent.includes('Edit')) {
        btn.textContent = '▶ Run Simulator';
        btn.style.background = '#4caf50';
        btn.onclick = () => runEmbeddedBlockSimulator(blockId, div.querySelector('strong')?.textContent || 'Simulator');
      } else if (btn.textContent.includes('Remove')) {
        btn.style.display = 'none';
      }
    });
  });
}

function runEmbeddedBlockSimulator(blockId, title) {
  // Find the block
  const block = courseBlocks.find((b) => b.id === blockId);
  if (!block) {
    alert("Simulator not found");
    return;
  }

  // Create popup window
  const popup = window.open(
    `http://localhost:5000/block-simulator.html?embedded=true&courseBlockId=${blockId}`,
    "block-simulator",
    "width=1200,height=800"
  );

  // Send block data to popup
  if (popup) {
    popup.onload = () => {
      popup.postMessage(
        {
          type: "loadEmbeddedBlocks",
          blocks: courseBlocks,
          blockId: blockId,
        },
        "*"
      );
    };
  }
}

function runEmbeddedVisualSimulator(blockId, title) {
  const block = courseBlocks.find((b) => b.id === blockId);
  if (!block) {
    alert("Simulator not found");
    return;
  }

  const popup = window.open(
    `http://localhost:5000/visual-simulator.html?embedded=true`,
    "visual-simulator",
    "width=1200,height=800"
  );

  if (popup) {
    popup.onload = () => {
      popup.postMessage(
        {
          type: "loadEmbeddedCode",
          code: block.data?.code || "",
          variables: block.data?.variables || {},
        },
        "*"
      );
    };
  }
}

function loadCourseSimulators(courseId) {
  // Display simulators from courseBlocks
  displayCourseSimulators(courseBlocks);
}

function displayCourseSimulators(blocks) {
  const viewerContent = document.getElementById("course-viewer-content");
  if (!blocks || blocks.length === 0) return;

  const simulatorSection = document.createElement("div");
  simulatorSection.style.marginTop = "30px";
  simulatorSection.innerHTML = "<h2>📊 Simulators</h2>";

  blocks.forEach((block) => {
    if (block.type.includes("simulator")) {
      const simulatorDiv = document.createElement("div");
      simulatorDiv.className = "simulator-block";
      simulatorDiv.dataset.blockId = block.id;
      simulatorDiv.style.cssText =
        "background: #f0f0f0; padding: 15px; margin: 10px 0; border-left: 4px solid #4caf50; border-radius: 4px;";
      simulatorDiv.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>${block.title}</strong>
                        <p style="margin: 5px 0; color: #666;">Type: ${block.type}</p>
                    </div>
                    <button type="button" style="padding: 8px 16px; background: #4caf50; color: white; border: none; border-radius: 4px; cursor: pointer;">▶ Run Simulator</button>
                </div>
            `;
      simulatorSection.appendChild(simulatorDiv);
    }
  });

  viewerContent.appendChild(simulatorSection);
}

function viewSimulator(simulatorId) {
  window.location.href = `http://localhost:5000/simulator-view.html?id=${simulatorId}`;
}

function deleteCourse(courseId) {
  if (!confirm("Are you sure?")) return;

  fetch(`http://localhost:3000/api/courses/${courseId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("Course deleted!");
        // INSTANT: Remove from array immediately
        myCourses = myCourses.filter((c) => c.id !== courseId);
        // INSTANT: Render immediately without reload
        renderUserCourses();
      } else {
        alert("Error: " + data.message);
      }
    })
    .catch((err) => {
      console.error("Error deleting course:", err);
      alert("Error deleting course. Check console.");
    });
}

function enrollInCourse(courseId) {
  fetch(`http://localhost:3000/api/courses/${courseId}/enroll`, {
    method: "POST",
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("Enrolled successfully!");
        // INSTANT: Update available courses list immediately
        availableCourses = availableCourses.filter((c) => c.id !== courseId);
        // INSTANT: Also reload in case there are other updates
        loadAvailableCourses();
        loadUserCourses();
      } else {
        alert("Error: " + data.message);
      }
    })
    .catch((err) => {
      console.error("Error enrolling:", err);
      alert("Error enrolling in course");
    });
}

function handleEditSimulator(event, blockId) {
  event.preventDefault();
  event.stopPropagation();

  const block = courseBlocks.find((b) => b.id === blockId);
  if (!block) {
    console.error("Block not found:", blockId);
    return;
  }

  console.log("Opening simulator for editing:", block);

  if (block.type === "block-simulator") {
    const popup = window.open(
      "http://localhost:5000/block-simulator.html?edit=true",
      "block-simulator-editor",
      "width=1400,height=900"
    );

    if (popup) {
      setTimeout(() => {
        popup.postMessage(
          {
            type: "load-simulator",
            blocks: block.data?.blocks || [],
            connections: block.data?.connections || [],
            blockTitle: block.title,
            courseBlockId: blockId,
          },
          "*"
        );
      }, 500);
    }
  } else if (block.type === "visual-simulator") {
    const popup = window.open(
      "http://localhost:5000/visual-simulator.html?edit=true",
      "visual-simulator-editor",
      "width=1200,height=800"
    );

    if (popup) {
      setTimeout(() => {
        popup.postMessage(
          {
            type: "load-code",
            code: block.data?.code || "",
            variables: block.data?.variables || {},
            courseBlockId: blockId,
          },
          "*"
        );
      }, 500);
    }
  }
}

function handleRemoveSimulator(event, blockId) {
  event.preventDefault();
  event.stopPropagation();

  if (!confirm("Remove this simulator from the course?")) return;

  courseBlocks = courseBlocks.filter((b) => b.id !== blockId);

  const simulatorDiv = document.querySelector(`[data-block-id="${blockId}"]`);
  if (simulatorDiv) {
    simulatorDiv.remove();
  }

  console.log("Simulator removed. Remaining blocks:", courseBlocks);
}

// ===== QUIZ FUNCTIONALITY =====
function setupQuizModalListeners() {
  const insertQuizBtn = document.getElementById('insert-quiz-question');
  const quizModal = document.getElementById('quiz-modal');
  const closeQuizModal = document.getElementById('close-quiz-modal');
  const cancelQuizModal = document.getElementById('cancel-quiz-modal');
  const quizForm = document.getElementById('quiz-question-form');
  const questionTypeSelect = document.getElementById('quiz-question-type');
  const optionsContainer = document.getElementById('quiz-options-container');
  const addOptionBtn = document.getElementById('add-quiz-option');

  if (insertQuizBtn) {
    insertQuizBtn.addEventListener('click', () => {
      if (!currentEditingCourseId) {
        alert('⚠️ Please save the course first ("Save as Draft") before adding quiz questions.');
        return;
      }
      openQuizModal();
    });
  }

  const deleteQuizBtn = document.getElementById('delete-quiz-question');
  if (deleteQuizBtn) {
    deleteQuizBtn.addEventListener('click', () => {
      if (currentEditingQuestionId) {
        console.log('🗑️ Modal delete button clicked for question:', currentEditingQuestionId);
        deleteQuizQuestion(currentEditingQuestionId);
      } else {
        console.warn('⚠️ No question selected for deletion');
      }
    });
  }

  if (closeQuizModal) {
    closeQuizModal.addEventListener('click', () => {
      closeQuizModalFunc();
    });
  }

  if (cancelQuizModal) {
    cancelQuizModal.addEventListener('click', () => {
      closeQuizModalFunc();
    });
  }

  if (quizForm) {
    quizForm.addEventListener('submit', (e) => {
      e.preventDefault();
      saveQuizQuestion();
    });
  }

  if (questionTypeSelect) {
    questionTypeSelect.addEventListener('change', (e) => {
      if (e.target.value === 'multiple_choice') {
        optionsContainer.style.display = 'block';
      } else {
        optionsContainer.style.display = 'none';
      }
    });
  }

  if (addOptionBtn) {
    addOptionBtn.addEventListener('click', () => {
      const optionsList = document.getElementById('quiz-options-list');
      const optionCount = optionsList.querySelectorAll('.quiz-option-input').length + 1;
      const newOption = document.createElement('input');
      newOption.type = 'text';
      newOption.className = 'quiz-option-input';
      newOption.placeholder = `Option ${optionCount}`;
      optionsList.appendChild(newOption);
    });
  }

  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === quizModal) {
      quizModal.style.display = 'none';
      resetQuizForm();
      currentEditingQuestionId = null;
    }
  });

  // Delegated listener for quiz placeholders in the editor
  const editor = document.getElementById('course-content-editor');
  if (editor) {
    // Handle delete button clicks
    editor.addEventListener('click', (e) => {
      const deleteBtn = e.target.closest('.quiz-placeholder-delete-btn');
      if (deleteBtn) {
        e.preventDefault();
        e.stopPropagation();
        const questionId = parseInt(deleteBtn.dataset.questionId);
        console.log(`🗑️ DELETE clicked for question:`, questionId);
        deleteQuizQuestion(questionId);
        return;
      }

      // Handle edit (click on placeholder, not on button)
      const placeholder = e.target.closest('.quiz-question-placeholder');
      if (placeholder && !e.target.closest('button')) {
        const questionId = placeholder.dataset.questionId;
        if (questionId) {
          console.log(`📝 EDIT clicked for question:`, questionId);
          openQuizModal(parseInt(questionId));
        }
      }
    });
  }
}

function openQuizModal(questionId = null) {
  const quizModal = document.getElementById('quiz-modal');
  const modalTitle = document.getElementById('quiz-modal-title');
  const deleteBtn = document.getElementById('delete-quiz-question');

  if (!quizModal) return;

  currentEditingQuestionId = questionId;

  if (questionId) {
    // Editing existing question
    modalTitle.textContent = 'Edit Quiz Question';
    if (deleteBtn) deleteBtn.style.display = 'inline-block';

    const question = courseQuestions.find(q => q.id === questionId);
    if (question) {
      document.getElementById('quiz-question-text').value = question.question_text;
      document.getElementById('quiz-question-type').value = question.question_type;
      document.getElementById('quiz-correct-answer').value = question.correct_answer;
      document.getElementById('quiz-explanation').value = question.explanation || '';
      document.getElementById('quiz-points').value = question.points;

      if (question.question_type === 'multiple_choice' && question.options) {
        const optionsList = document.getElementById('quiz-options-list');
        optionsList.innerHTML = '';
        question.options.forEach((option, index) => {
          const input = document.createElement('input');
          input.type = 'text';
          input.className = 'quiz-option-input';
          input.placeholder = `Option ${index + 1}`;
          input.value = option;
          optionsList.appendChild(input);
        });
        document.getElementById('quiz-options-container').style.display = 'block';
      } else {
        document.getElementById('quiz-options-container').style.display = 'none';
      }
    }
  } else {
    // Creating new question
    modalTitle.textContent = 'Add Quiz Question';
    if (deleteBtn) deleteBtn.style.display = 'none';
    resetQuizForm();
  }

  quizModal.style.display = 'block';
}

function closeQuizModalFunc() {
  const quizModal = document.getElementById('quiz-modal');
  if (quizModal) {
    quizModal.style.display = 'none';
    resetQuizForm();
    currentEditingQuestionId = null;
  }
}

function resetQuizForm() {
  document.getElementById('quiz-question-text').value = '';
  document.getElementById('quiz-question-type').value = 'multiple_choice';
  document.getElementById('quiz-correct-answer').value = '';
  document.getElementById('quiz-explanation').value = '';
  document.getElementById('quiz-points').value = '10';

  const optionsList = document.getElementById('quiz-options-list');
  if (optionsList) {
    optionsList.innerHTML = `
      <input type="text" class="quiz-option-input" placeholder="Option 1" />
      <input type="text" class="quiz-option-input" placeholder="Option 2" />
      <input type="text" class="quiz-option-input" placeholder="Option 3" />
      <input type="text" class="quiz-option-input" placeholder="Option 4" />
    `;
  }

  const optionsContainer = document.getElementById('quiz-options-container');
  if (optionsContainer) {
    optionsContainer.style.display = 'block';
  }
}

async function saveQuizQuestion() {
  const questionText = document.getElementById('quiz-question-text').value.trim();
  const questionType = document.getElementById('quiz-question-type').value;
  const correctAnswer = document.getElementById('quiz-correct-answer').value.trim();
  const explanation = document.getElementById('quiz-explanation').value.trim();
  const points = parseInt(document.getElementById('quiz-points').value);

  if (!questionText || !correctAnswer) {
    alert('Please fill in the question text and correct answer');
    return;
  }

  let options = null;
  if (questionType === 'multiple_choice') {
    const optionInputs = document.querySelectorAll('.quiz-option-input');
    options = Array.from(optionInputs)
      .map(input => input.value.trim())
      .filter(val => val !== '');

    if (options.length < 2) {
      alert('Please provide at least 2 options for multiple choice questions');
      return;
    }
  }

  const questionData = {
    question_text: questionText,
    question_type: questionType,
    options: options,
    correct_answer: correctAnswer,
    explanation: explanation,
    points: points,
    order_index: courseQuestions.length
  };

  try {
    let response;
    if (currentEditingQuestionId) {
      response = await fetch(`http://localhost:3000/api/courses/${currentEditingCourseId}/questions/${currentEditingQuestionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(questionData)
      });
    } else {
      response = await fetch(`http://localhost:3000/api/courses/${currentEditingCourseId}/questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(questionData)
      });
    }

    const result = await response.json();

    if (result.success) {
      alert(currentEditingQuestionId ? 'Question updated successfully!' : 'Question added successfully!');
      closeQuizModalFunc();
      await loadCourseQuestions(currentEditingCourseId);

      const editor = document.getElementById('course-content-editor');

      // Clear ALL placeholders to prevent duplicates
      const allPlaceholders = editor.querySelectorAll('.quiz-question-placeholder');
      allPlaceholders.forEach(p => p.remove());

      // Re-render all quiz question placeholders from loaded questions
      courseQuestions.forEach(q => {
        insertQuizPlaceholder(q.question_text, q.id);
      });
    } else {
      alert('Error saving question: ' + result.message);
    }
  } catch (error) {
    console.error('Error saving quiz question:', error);
    alert('Error saving question. Please try again.');
  }
}

function insertQuizPlaceholder(questionText, questionId) {
  const editor = document.getElementById('course-content-editor');
  const placeholder = document.createElement('div');
  placeholder.className = 'quiz-question-placeholder';
  placeholder.dataset.questionId = questionId || '';
  placeholder.contentEditable = 'false'; // Make it non-editable
  placeholder.style.cssText = 'background: rgba(102, 126, 234, 0.2); border: 2px dashed var(--primary); padding: 1em; margin: 1em 0; border-radius: 4px; position: relative; cursor: pointer; user-select: none;';

  let deleteBtnHtml = '';
  if (questionId) {
    deleteBtnHtml = `<button type="button" class="quiz-placeholder-delete-btn" data-question-id="${questionId}" style="position: absolute; top: 5px; right: 5px; background: #e53e3e; color: white; border: none; border-radius: 4px; padding: 2px 6px; cursor: pointer; font-size: 0.8em; z-index: 10;">🗑️ Delete</button>`;
  }

  placeholder.innerHTML = `
    <strong>❓ Quiz Question:</strong> ${questionText.substring(0, 100)}${questionText.length > 100 ? '...' : ''}
    ${deleteBtnHtml}
    <div style="font-size: 0.85em; color: #999; margin-top: 0.5em;">Click to edit</div>
  `;

  // Click handler for editing (click anywhere except button)
  placeholder.addEventListener('click', (e) => {
    if (e.target.closest('button')) return; // Let button handle itself

    const qId = placeholder.dataset.questionId;
    if (qId) {
      openQuizModal(parseInt(qId));
    }
  });

  editor.appendChild(placeholder);
}

async function deleteQuizQuestion(questionId, btnElement = null) {
  console.log(`🗑️ Delete button clicked for question ID:`, questionId);
  console.log(`   currentEditingCourseId:`, currentEditingCourseId);
  console.log(`   authToken exists:`, !!authToken);

  if (!currentEditingCourseId) {
    alert('❌ Error: Course ID not set. Please save the course first.');
    return;
  }

  // Store question data for undo BEFORE deleting
  const questionToDelete = courseQuestions.find(q => q.id === questionId);
  if (questionToDelete) {
    lastDeletedQuestion = {
      question_text: questionToDelete.question_text,
      question_type: questionToDelete.question_type,
      options: questionToDelete.options,
      correct_answer: questionToDelete.correct_answer,
      explanation: questionToDelete.explanation,
      points: questionToDelete.points
    };
    console.log('💾 Stored question for undo:', lastDeletedQuestion);
  }

  // REMOVED confirmation dialog - it wasn't showing and was auto-cancelling
  // User can press Ctrl+Z to undo if they delete by accident
  console.log(`🗑️ Proceeding with deletion of question ID:`, questionId);

  try {
    const url = `http://localhost:3000/api/courses/${currentEditingCourseId}/questions/${questionId}`;
    console.log(`   API URL:`, url);

    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    console.log(`   Response status:`, response.status);
    const result = await response.json();
    console.log(`   Delete response:`, result);

    if (result.success) {
      alert('Question deleted! Press Ctrl+Z to undo.');
      closeQuizModalFunc();

      // Remove from courseQuestions array
      courseQuestions = courseQuestions.filter(q => q.id !== questionId);
      console.log(`✓ Removed from array. Remaining questions:`, courseQuestions.length);

      // Remove placeholder from DOM by data attribute
      const editor = document.getElementById('course-content-editor');
      const placeholders = editor.querySelectorAll('.quiz-question-placeholder');
      console.log(`📌 Found ${placeholders.length} placeholders in editor`);

      // Match by data attribute value as string
      let removed = false;
      placeholders.forEach(p => {
        const pId = p.dataset.questionId;
        console.log(`  Checking placeholder with ID: "${pId}" vs "${questionId}"`);
        if (pId == questionId) {  // Use == to handle string/number comparison
          p.remove();
          removed = true;
          console.log(`  ✓ Removed placeholder`);
        }
      });

      if (!removed) {
        console.warn(`⚠️ Warning: Placeholder not found for ID ${questionId}`);
      }
    } else {
      console.error(`❌ Delete failed:`, result.message);
      alert('Error deleting question: ' + result.message);
      lastDeletedQuestion = null; // Clear if delete failed
    }
  } catch (error) {
    console.error('❌ Error deleting question:', error);
    alert('Error deleting question: ' + error.message);
    lastDeletedQuestion = null; // Clear if error
  }
}

async function loadCourseQuestions(courseId) {
  try {
    const response = await fetch(`http://localhost:3000/api/courses/${courseId}/questions`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    const result = await response.json();
    if (result.success) {
      courseQuestions = result.data;
      console.log(`Loaded ${courseQuestions.length} questions for course ${courseId}`);
    }
  } catch (error) {
    console.error('Error loading course questions:', error);
  }
}

async function renderQuizQuestionsInViewer(courseId) {
  await loadCourseQuestions(courseId);

  if (courseQuestions.length === 0) {
    return;
  }

  const viewerContent = document.getElementById('course-viewer-content');
  const quizSection = document.createElement('div');
  quizSection.className = 'quiz-section';
  quizSection.innerHTML = '<h3 style="color: var(--accent); margin-top: 2em;">📝 Quiz Questions</h3>';

  courseQuestions.forEach((question, index) => {
    const questionEl = createQuizQuestionElement(question, index);
    quizSection.appendChild(questionEl);
  });

  viewerContent.appendChild(quizSection);
}

function createQuizQuestionElement(question, index) {
  const questionDiv = document.createElement('div');
  questionDiv.className = 'quiz-question';
  questionDiv.dataset.questionId = question.id;

  let optionsHTML = '';
  if (question.question_type === 'multiple_choice' && question.options) {
    optionsHTML = '<div class="quiz-options">';
    question.options.forEach((option, optIndex) => {
      optionsHTML += `
        <div class="quiz-option">
          <input type="radio" name="question-${question.id}" id="q${question.id}-opt${optIndex}" value="${option}">
          <label for="q${question.id}-opt${optIndex}">${option}</label>
        </div>
      `;
    });
    optionsHTML += '</div>';
  } else if (question.question_type === 'true_false') {
    optionsHTML = `
      <div class="quiz-options">
        <div class="quiz-option">
          <input type="radio" name="question-${question.id}" id="q${question.id}-true" value="True">
          <label for="q${question.id}-true">True</label>
        </div>
        <div class="quiz-option">
          <input type="radio" name="question-${question.id}" id="q${question.id}-false" value="False">
          <label for="q${question.id}-false">False</label>
        </div>
      </div>
    `;
  } else {
    optionsHTML = `
      <input type="text" id="q${question.id}-answer" placeholder="Enter your answer" style="width: 100%; padding: 0.8em; margin: 1em 0; border: 1px solid var(--primary); border-radius: 4px; background: rgba(255,255,255,0.05); color: var(--light);">
    `;
  }

  questionDiv.innerHTML = `
    <div class="quiz-question-header">
      <div class="quiz-question-text">Question ${index + 1}: ${question.question_text}</div>
      <div class="quiz-points">${question.points} pts</div>
    </div>
    ${optionsHTML}
    <button class="quiz-submit-btn" onclick="submitQuizAnswer(${question.id})">Submit Answer</button>
    <div id="feedback-${question.id}" class="quiz-feedback" style="display: none;"></div>
  `;

  return questionDiv;
}

async function submitQuizAnswer(questionId) {
  const question = courseQuestions.find(q => q.id === questionId);
  if (!question) return;

  let userAnswer;
  if (question.question_type === 'short_answer') {
    userAnswer = document.getElementById(`q${questionId}-answer`).value.trim();
  } else {
    const selectedOption = document.querySelector(`input[name="question-${questionId}"]:checked`);
    if (!selectedOption) {
      alert('Please select an answer');
      return;
    }
    userAnswer = selectedOption.value;
  }

  if (!userAnswer) {
    alert('Please provide an answer');
    return;
  }

  try {
    const response = await fetch(`http://localhost:3000/api/courses/${currentEditingCourseId}/questions/${questionId}/answer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify({ user_answer: userAnswer })
    });

    const result = await response.json();

    if (result.success) {
      const feedbackDiv = document.getElementById(`feedback-${questionId}`);
      feedbackDiv.style.display = 'block';

      if (result.data.is_correct) {
        feedbackDiv.className = 'quiz-feedback correct';
        feedbackDiv.innerHTML = `
          <div>✅ Correct!</div>
          ${result.data.explanation ? `<div class="quiz-explanation">${result.data.explanation}</div>` : ''}
        `;
      } else {
        feedbackDiv.className = 'quiz-feedback incorrect';
        feedbackDiv.innerHTML = `
          <div>❌ Incorrect. The correct answer is: ${result.data.correct_answer}</div>
          ${result.data.explanation ? `<div class="quiz-explanation">${result.data.explanation}</div>` : ''}
        `;
      }

      const submitBtn = feedbackDiv.previousElementSibling;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Answered';
    } else {
      alert('Error submitting answer: ' + result.message);
    }
  } catch (error) {
    console.error('Error submitting answer:', error);
    alert('Error submitting answer. Please try again.');
  }
}

// Make functions globally accessible
window.submitQuizAnswer = submitQuizAnswer;
window.deleteQuizQuestion = deleteQuizQuestion;
