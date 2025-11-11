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

// ===== INITIALIZATION =====
document.addEventListener("DOMContentLoaded", () => {
  initializeApp();
});

function initializeApp() {
  setupAuthListeners();
  setupNavigationListeners();
  setupCourseEditorListeners();

  if (authToken) {
    fetchUserProfile();
  } else {
    showAuthSection();
  }
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
        currentUser = data.data;
        showDashboard();
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

  if (courseForm) {
    courseForm.addEventListener("submit", (e) => {
      e.preventDefault();
      saveCourse();
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
                        <div style="padding: 10px; border: 1px solid #ddd; margin: 10px 0; border-radius: 4px; cursor: pointer;" onclick="selectSimulatorForCourse(${
                          sim.id
                        }, '${type}', '${sim.title.replace(/'/g, "\\'")}')">
                            <strong>${sim.title}</strong>
                            <p style="margin: 5px 0; font-size: 0.9em; color: #666;">${
                              sim.description || "No description"
                            }</p>
                            <p style="margin: 5px 0; font-size: 0.8em; color: #999;">by ${
                              sim.creator_email
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

  // Determine which dashboard to show
  if (currentUser?.role === "superadmin") {
    showSuperadminDashboard();
  } else if (currentUser?.role === "admin") {
    showAdminDashboard();
  } else {
    showUserDashboard();
  }
}

function showSuperadminDashboard() {
  document.getElementById("user-dashboard").style.display = "none";
  document.getElementById("admin-dashboard").style.display = "none";
  document.getElementById("superadmin-dashboard").style.display = "block";

  loadAllUsers();
  loadPendingCourses();
  loadUserCourses();
  loadAvailableCourses();

  document
    .getElementById("create-course-button-superadmin")
    ?.addEventListener("click", createNewCourse);
}

function showAdminDashboard() {
  document.getElementById("user-dashboard").style.display = "none";
  document.getElementById("superadmin-dashboard").style.display = "none";
  document.getElementById("admin-dashboard").style.display = "block";

  loadPendingCourses();
  loadUserCourses();
  loadAvailableCourses();

  document
    .getElementById("create-course-button-admin")
    ?.addEventListener("click", createNewCourse);
}

function showUserDashboard() {
  document.getElementById("superadmin-dashboard").style.display = "none";
  document.getElementById("admin-dashboard").style.display = "none";
  document.getElementById("user-dashboard").style.display = "block";

  loadUserCourses();
  loadAvailableCourses();

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
            <strong>${course.title}</strong> by ${course.creator_id}
            <p>${course.description}</p>
            <button onclick="approveCourse(${course.id})">Approve</button>
            <button onclick="rejectCourse(${course.id})">Reject</button>
        </li>
    `
    )
    .join("");
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
        alert("Course approved and is now visible to all users!");
        loadPendingCourses();
        loadAvailableCourses(); // Refresh available courses list
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
        alert("Course rejected");
        loadPendingCourses();
      }
    })
    .catch((err) => console.error("Error rejecting course:", err));
}

function loadUserCourses() {
  fetch("http://localhost:3000/api/courses", {
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        console.log("=== LOAD USER COURSES DEBUG ===");
        console.log("Current user ID:", currentUser.id, "Type:", typeof currentUser.id);
        console.log("All courses from API:", data.data);
        // Show own courses regardless of status (creator can always see their courses)
        myCourses = data.data.filter((c) => parseInt(c.creator_id) === parseInt(currentUser.id));
        console.log("Filtered user courses:", myCourses);
        console.log("Number of user courses:", myCourses.length);
        renderUserCourses();
      }
    })
    .catch((err) => console.error("Error loading courses:", err));
}

function loadAvailableCourses() {
  fetch("http://localhost:3000/api/courses", {
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        console.log("=== LOAD AVAILABLE COURSES DEBUG ===");
        console.log("Current user ID:", currentUser.id, "Type:", typeof currentUser.id);
        console.log("All courses from API:", data.data);
        // Show approved courses from OTHER creators (not self)
        const approvedCourses = data.data.filter(
          (c) => {
            const isApproved = c.status === "approved";
            const isNotOwner = parseInt(c.creator_id) !== parseInt(currentUser.id);
            console.log(`Course "${c.title}" - Status: ${c.status}, Creator ID: ${c.creator_id}, IsApproved: ${isApproved}, IsNotOwner: ${isNotOwner}`);
            return isApproved && isNotOwner;
          }
        );
        console.log("Filtered approved courses (from other creators):", approvedCourses);
        availableCourses = approvedCourses;
        renderAvailableCourses();
      } else {
        console.error("API Error:", data.message);
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

    if (myCourses.length === 0) {
      list.innerHTML = "<li><em>No courses created yet</em></li>";
      return;
    }

    list.innerHTML = myCourses
      .map(
        (course) => `
<li>
<strong>${course.title}</strong>
<p>${course.description || "No description"}</p>
<p style="font-size: 0.9em; color: #999;">Status: <span style="background: ${
          course.status === "pending"
            ? "#ffa500"
            : course.status === "approved"
            ? "#4caf50"
            : "#f44336"
        }; color: white; padding: 2px 6px; border-radius: 3px;">${
          course.status
        }</span></p>
<button onclick="editCourse(${course.id})">Edit</button>
<button onclick="viewCourse(${course.id})">View</button>
<button onclick="deleteCourse(${course.id})">Delete</button>
</li>
`
      )
      .join("");
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

    if (availableCourses.length === 0) {
      list.innerHTML = "<li><em>No courses available to enroll in</em></li>";
      return;
    }

    list.innerHTML = availableCourses
      .map(
        (course) => `
<li>
<strong>${course.title}</strong>
<p>${course.description || "No description"}</p>
<p style="font-size: 0.85em; color: #666;">by ${course.creator_email}</p>
<button onclick="enrollInCourse(${course.id})">Enroll</button>
    <button onclick="viewCourse(${course.id})">Preview</button>
    </li>
    `
      )
      .join("");
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

    courseBlocks = [];

    document.getElementById("dashboard-section").style.display = "none";
    document.getElementById("course-editor-section").style.display = "block";
  }
}

function saveCourse() {
  const title = document.getElementById("course-title").value;
  const description = document.getElementById("course-description").value;
  const content = document.getElementById("course-content-editor").innerHTML;

  if (!title.trim()) {
    alert("Please enter a course title");
    return;
  }

  const courseData = {
    title,
    description,
    content,
    blocks: courseBlocks,
  };

  const method = currentEditingCourseId ? "PUT" : "POST";
  const url = currentEditingCourseId
    ? `http://localhost:3000/api/courses/${currentEditingCourseId}`
    : "http://localhost:3000/api/courses";

  fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${authToken}`,
    },
    body: JSON.stringify(courseData),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        const courseId = currentEditingCourseId || data.data.id;

        // Save simulators to course
        const simulatorPromises = courseBlocks
          .filter((block) => block.simulatorId)
          .map((block) =>
            fetch(`http://localhost:3000/api/courses/${courseId}/simulators`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${authToken}`,
              },
              body: JSON.stringify({ simulator_id: block.simulatorId }),
            })
          );

        Promise.all(simulatorPromises)
          .then(() => {
            alert("Course saved successfully!");
            showDashboard();
          })
          .catch((err) => {
            console.error("Error saving simulators to course:", err);
            alert("Course saved but error linking simulators");
            showDashboard();
          });
      } else {
        alert("Error saving course: " + (data.message || "Unknown error"));
      }
    })
    .catch((err) => {
      console.error("Error saving course:", err);
      alert("Error saving course");
    });
}

function viewCourse(courseId) {
  const course = [...myCourses, ...availableCourses].find(
    (c) => c.id === courseId
  );
  if (!course) return;

  document.getElementById("course-viewer-title").textContent = course.title;
  document.getElementById("course-viewer-description").textContent =
    course.description || "";
  document.getElementById("course-viewer-content").innerHTML =
    course.content || "";

  // Load and display simulators for this course
  loadCourseSimulators(courseId);

  document.getElementById("dashboard-section").style.display = "none";
  document.getElementById("course-viewer-section").style.display = "block";
}

function loadCourseSimulators(courseId) {
  const authToken = localStorage.getItem("token");
  
  fetch(`http://localhost:3000/api/courses/${courseId}/simulators`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success && data.data && data.data.length > 0) {
        displayCourseSimulators(data.data);
      } else {
        document.getElementById("course-simulators-section").style.display = "none";
      }
    })
    .catch((err) => {
      console.error("Error loading course simulators:", err);
      document.getElementById("course-simulators-section").style.display = "none";
    });
}

function displayCourseSimulators(simulators) {
  const simulatorsSection = document.getElementById("course-simulators-section");
  const simulatorsList = document.getElementById("course-simulators-list");
  
  if (!simulators || simulators.length === 0) {
    simulatorsSection.style.display = "none";
    return;
  }
  
  simulatorsList.innerHTML = simulators
    .map(
      (sim) => `
        <div style="background: #f5f5f5; padding: 1em; border-radius: 6px; cursor: pointer; transition: transform 0.2s;" onclick="viewSimulator(${sim.id})">
          <h4 style="margin: 0 0 0.5em 0; color: #333;">${sim.title || "Untitled Simulator"}</h4>
          <p style="margin: 0; font-size: 0.9em; color: #666;">${sim.description || "No description"}</p>
          <div style="margin-top: 0.5em; font-size: 0.85em; color: #999;">
            <span>⭐ ${sim.rating_avg || "0"} | 👥 ${sim.downloads || "0"} downloads</span>
          </div>
          <button style="margin-top: 0.5em; padding: 0.5em 1em; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; width: 100%;">
            Run Simulator
          </button>
        </div>
      `
    )
    .join("");
  
  simulatorsSection.style.display = "block";
}

function viewSimulator(simulatorId) {
  // Navigate to simulator view/execution page
  window.location.href = `simulator-view.html?id=${simulatorId}`;
}

function deleteCourse(courseId) {
  if (!confirm("Are you sure you want to delete this course?")) return;

  fetch(`http://localhost:3000/api/courses/${courseId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("Course deleted");
        showDashboard();
      }
    })
    .catch((err) => console.error("Error deleting course:", err));
}

function enrollInCourse(courseId) {
  fetch(`http://localhost:3000/api/courses/${courseId}/enroll`, {
    method: "POST",
    headers: { Authorization: `Bearer ${authToken}` },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("Enrolled in course!");
        loadUserCourses();
      }
    })
    .catch((err) => console.error("Error enrolling:", err));
}

// ===== SIMULATOR HANDLERS =====
function handleEditSimulator(event, blockId) {
  const block = courseBlocks.find((b) => b.id === blockId);
  if (!block) return;

  if (block.type === "visual-simulator") {
    currentEditingSimulatorBlockId = blockId;
    const win = window.open(
      "visual-simulator.html",
      "visual-sim-editor",
      "width=1200,height=800"
    );
    win.addEventListener("load", () => {
      win.postMessage({ type: "load-simulator", data: block.data }, "*");
    });
  } else if (block.type === "block-simulator") {
    currentEditingSimulatorBlockId = blockId;
    // Open in new window so exitSimulator can use window.opener
    window.open("block-simulator.html", "BlockSimulator", "width=1200,height=800");
  } else {
    alert("Editing for this simulator type coming soon");
  }
}

function handleRemoveSimulator(event, blockId) {
  if (confirm("Remove this simulator?")) {
    courseBlocks = courseBlocks.filter((b) => b.id !== blockId);
    event.target.closest(".simulator-block").remove();
  }
}

// Receive simulator data from child windows
window.addEventListener("message", (event) => {
  if (event.data.type === "save-simulator") {
    const block = courseBlocks.find(
      (b) => b.id === currentEditingSimulatorBlockId
    );
    if (block) {
      block.data = event.data.data;
      console.log("Simulator data saved:", block);
    }
  }

  // Handle close message from block simulator
  if (event.data.type === "closeBlockSimulator") {
    console.log("Block simulator closed");
    showDashboard();
  }
});
