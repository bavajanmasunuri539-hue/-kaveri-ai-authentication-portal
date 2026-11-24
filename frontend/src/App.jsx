import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";

function App() {
  const resetToken = new URLSearchParams(window.location.search).get("token");

  const [mode, setMode] = useState(
    resetToken ? "reset" : "login"
  );
  const [showPassword, setShowPassword] = useState(false);
  const [user, setUser] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const isLogin = mode === "login";

  useEffect(() => {
    async function checkAuthentication() {
      try {
        const response = await fetch(`${API_URL}/auth/google/me`, {
          method: "GET",
          credentials: "include"
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data.user);
        }
      } catch (err) {
        setError("Unable to connect to the authentication server.");
      } finally {
        setAuthChecked(true);
      }
    }

    checkAuthentication();
  }, []);

  function changeMode(newMode) {
    setMode(newMode);
    setError("");
    setSuccess("");
    setShowPassword(false);
  }

  async function handleLogout() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/auth/google/logout`, {
        method: "POST",
        credentials: "include"
      });

      if (!response.ok) {
        throw new Error("Logout failed.");
      }

      setUser(null);
      changeMode("login");
    } catch (err) {
      setError("Unable to logout. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    const formData = new FormData(e.currentTarget);

    try {
      const endpoint = isLogin
        ? "/auth/email/login"
        : "/auth/email/register";

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          email: formData.get("email").trim(),
          password: formData.get("password")
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Authentication failed.");
      }

      setUser(data.user);
      setError("");
      e.target.reset();

    } catch (err) {
      setError(err.message || "Unable to connect to server.");
    } finally {
      setLoading(false);
    }
  }

  async function handleForgotPassword(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    const formData = new FormData(e.currentTarget);

    try {
      const response = await fetch(`${API_URL}/auth/password/forgot`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: formData.get("email").trim()
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to process request.");
      }

      setSuccess(data.message);
      e.target.reset();

    } catch (err) {
      setError(err.message || "Unable to connect to server.");
    } finally {
      setLoading(false);
    }
  }

  async function handleResetPassword(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    const formData = new FormData(e.currentTarget);
    const newPassword = formData.get("new_password");
    const confirmPassword = formData.get("confirm_password");

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/auth/password/reset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token: resetToken,
          new_password: newPassword
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Password reset failed.");
      }

      setSuccess(data.message);
      e.target.reset();

      window.history.replaceState({}, "", "/");
      changeMode("login");
      setSuccess(data.message);

    } catch (err) {
      setError(err.message || "Unable to connect to server.");
    } finally {
      setLoading(false);
    }
  }

  if (!authChecked) {
    return (
      <div className="app">
        <h2>Checking authentication...</h2>
      </div>
    );
  }

  const showPasswordPage = mode === "forgot" || mode === "reset";

  return (
    <div className="app">
      <header className="header">
        <div className="logo">KAVERI <b>AI</b></div>
        <p>Intelligent Solutions. Secure Experiences.</p>
      </header>

      <main className="main">
        {user && !showPasswordPage ? (
          <section className="auth-card">
            <h2>Welcome to KAVERI AI!</h2>
            <p className="description">
              You are successfully authenticated.
            </p>

            <div className="features">
              <div>Account Email: {user.email}</div>
              <div>Authentication: Secure Authentication</div>
              <div>Account Status: Active</div>
            </div>

            {error && <p role="alert">{error}</p>}

            <button
              className="primary"
              onClick={handleLogout}
              disabled={loading}
            >
              {loading ? "Logging out..." : "Logout"}
            </button>
          </section>
        ) : (
          <>
            <section className="hero">
              <div className="hero-content">
                <h1>Welcome to<br /><span>KAVERI AI</span></h1>
                <p>
                  Experience secure, simple and intelligent access to your digital workspace.
                </p>

                <div className="features">
                  <div><span>01</span> Secure Authentication</div>
                  <div><span>02</span> Protected User Accounts</div>
                  <div><span>03</span> Google Sign-In Integration</div>
                </div>
              </div>
            </section>

            <section className="auth-card">

              {mode === "login" || mode === "signup" ? (
                <>
                  <div className="tabs">
                    <button
                      className={isLogin ? "selected" : ""}
                      onClick={() => changeMode("login")}
                    >
                      Login
                    </button>

                    <button
                      className={!isLogin ? "selected" : ""}
                      onClick={() => changeMode("signup")}
                    >
                      Sign Up
                    </button>
                  </div>

                  <h2>{isLogin ? "Welcome Back!" : "Create Account"}</h2>

                  <p className="description">
                    {isLogin
                      ? "Login to access your secure workspace."
                      : "Register your KAVERI AI account."}
                  </p>

                  {error && <p role="alert">{error}</p>}
                  {success && <p role="status">{success}</p>}

                  <form onSubmit={handleSubmit}>
                    {!isLogin && (
                      <label>
                        Full Name
                        <input
                          type="text"
                          name="full_name"
                          placeholder="Enter your full name"
                          required
                        />
                      </label>
                    )}

                    <label>
                      Email Address
                      <input
                        type="email"
                        name="email"
                        placeholder="Enter your email address"
                        required
                      />
                    </label>

                    <label>
                      Password
                      <div className="password-field">
                        <input
                          type={showPassword ? "text" : "password"}
                          name="password"
                          placeholder="Enter your password"
                          minLength="8"
                          required
                        />

                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                        >
                          {showPassword ? "Hide" : "Show"}
                        </button>
                      </div>
                    </label>

                    {isLogin && (
                      <button
                        type="button"
                        className="forgot"
                        onClick={() => changeMode("forgot")}
                      >
                        Forgot password?
                      </button>
                    )}

                    <button className="primary" type="submit" disabled={loading}>
                      {loading
                        ? "Please wait..."
                        : isLogin
                          ? "Login to Account"
                          : "Create Account"}
                    </button>
                  </form>

                  <div className="divider">
                    <span>OR CONTINUE WITH</span>
                  </div>

                  <button
                    className="google"
                    onClick={() => {
                      window.location.href = `${API_URL}/auth/google/login`;
                    }}
                  >
                    <b>G</b> Continue with Google
                  </button>

                  <div className="switch">
                    {isLogin
                      ? "Don't have an account?"
                      : "Already have an account?"}

                    <button
                      onClick={() => changeMode(isLogin ? "signup" : "login")}
                    >
                      {isLogin ? "Sign Up" : "Login"}
                    </button>
                  </div>
                </>
              ) : mode === "forgot" ? (
                <>
                  <h2>Forgot Password?</h2>

                  <p className="description">
                    Enter your registered email address. We'll send you a password-reset link.
                  </p>

                  {error && <p role="alert">{error}</p>}
                  {success && <p role="status">{success}</p>}

                  <form onSubmit={handleForgotPassword}>
                    <label>
                      Email Address
                      <input
                        type="email"
                        name="email"
                        placeholder="Enter your registered email"
                        required
                      />
                    </label>

                    <button className="primary" type="submit" disabled={loading}>
                      {loading ? "Sending..." : "Send Reset Link"}
                    </button>
                  </form>

                  <div className="switch">
                    Remember your password?
                    <button onClick={() => changeMode("login")}>
                      Back to Login
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <h2>Reset Password</h2>

                  <p className="description">
                    Enter your new password below.
                  </p>

                  {error && <p role="alert">{error}</p>}
                  {success && <p role="status">{success}</p>}

                  <form onSubmit={handleResetPassword}>
                    <label>
                      New Password
                      <input
                        type="password"
                        name="new_password"
                        placeholder="Enter new password"
                        minLength="8"
                        maxLength="128"
                        required
                      />
                    </label>

                    <label>
                      Confirm Password
                      <input
                        type="password"
                        name="confirm_password"
                        placeholder="Confirm new password"
                        minLength="8"
                        maxLength="128"
                        required
                      />
                    </label>

                    <button className="primary" type="submit" disabled={loading}>
                      {loading ? "Resetting..." : "Reset Password"}
                    </button>
                  </form>

                  <div className="switch">
                    <button onClick={() => changeMode("login")}>
                      Back to Login
                    </button>
                  </div>
                </>
              )}
            </section>
          </>
        )}
      </main>

      <footer>Copyright 2026 KAVERI AI. All rights reserved.</footer>
    </div>
  );
}

export default App;
