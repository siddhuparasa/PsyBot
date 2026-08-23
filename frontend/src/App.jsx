import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedMood, setSelectedMood] = useState("");

  const sendMessage = async (customMessage = null) => {
    const text = (customMessage || message).trim();

    if (!text || loading) return;

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: text,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: text,
      });

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "bot",
          content: response.data.response,
        },
      ]);
    } catch (error) {
      console.error("PsyBot error:", error);

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "bot",
          content:
            "I'm unable to respond right now. Please try again in a moment.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setMessage("");
    setSelectedMood("");
  };

  const selectMood = (mood) => {
    setSelectedMood(mood);

    const moodMessages = {
      Calm:
        "I'm feeling calm today and would like to reflect on my thoughts.",

      Anxious:
        "I've been feeling anxious lately and I'd like to understand what I'm experiencing.",

      Low:
        "I've been feeling low lately and I'm not sure how to deal with it.",

      Stressed:
        "I've been feeling stressed and overwhelmed recently.",

      Frustrated:
        "I've been feeling frustrated lately and I'd like to talk about it.",

      Unsure:
        "I'm not really sure how I'm feeling right now.",
    };

    setMessage(moodMessages[mood]);
  };

  return (
    <div className="app">

      {/* ==================================================
          NAVBAR
      ================================================== */}

      <header className="navbar">

        <button
          className="brand"
          onClick={clearChat}
          aria-label="Go to PsyBot home"
        >

          <div className="brand-icon">
            🧠
          </div>

          <div className="brand-text">

            <h1>
              PsyBot
            </h1>

            <span>
              Psychology Support Assistant
            </span>

          </div>

        </button>


        {messages.length > 0 && (

          <button
            className="clear-button"
            onClick={clearChat}
          >
            New conversation
          </button>

        )}

      </header>


      {/* ==================================================
          MAIN
      ================================================== */}

      <main className="main">

        {messages.length === 0 ? (

          <>
            {/* ==================================================
                HERO
            ================================================== */}

            <section className="hero">

              <div className="hero-badge">
                Psychology • Emotional Well-being
              </div>

              <h2>
                Understand your thoughts.
                <span>
                  Explore your emotions.
                </span>
              </h2>

              <p>
                PsyBot is a psychology-focused support
                assistant for exploring emotions, stress,
                relationships, self-esteem and everyday
                mental well-being.
              </p>

            </section>


            {/* ==================================================
                EMOTIONAL CHECK-IN
            ================================================== */}

            <section className="checkin-card">

              <div className="checkin-header">

                <div>

                  <span className="section-label">
                    EMOTIONAL CHECK-IN
                  </span>

                  <h3>
                    How are you feeling today?
                  </h3>

                </div>

                <div className="checkin-mark">
                  ✦
                </div>

              </div>


              {/* MOODS */}

              <div className="mood-grid">

                {[
                  ["😌", "Calm"],
                  ["😟", "Anxious"],
                  ["😔", "Low"],
                  ["😣", "Stressed"],
                  ["😤", "Frustrated"],
                  ["😶", "Unsure"],
                ].map(([emoji, mood]) => (

                  <button
                    key={mood}
                    className={`mood-card ${
                      selectedMood === mood
                        ? "selected"
                        : ""
                    }`}
                    onClick={() => selectMood(mood)}
                  >

                    <span className="mood-emoji">
                      {emoji}
                    </span>

                    <span>
                      {mood}
                    </span>

                  </button>

                ))}

              </div>


              {/* SELECTED MOOD */}

              {selectedMood && (

                <div className="selected-message">

                  <span>
                    Your starting point:
                  </span>

                  <strong>
                    {selectedMood}
                  </strong>

                </div>

              )}


              {/* MESSAGE INPUT */}

              <div className="checkin-input">

                <textarea
                  value={message}
                  onChange={(event) =>
                    setMessage(event.target.value)
                  }
                  onKeyDown={handleKeyDown}
                  placeholder="Or describe what's on your mind..."
                  rows="2"
                  disabled={loading}
                />

                <button
                  className="checkin-send"
                  onClick={() => sendMessage()}
                  disabled={
                    !message.trim() || loading
                  }
                >
                  {loading
                    ? "..."
                    : "Start conversation →"}
                </button>

              </div>

            </section>


            {/* ==================================================
                ABOUT
            ================================================== */}

            <section className="about-strip">

              <div className="about-icon">
                ◌
              </div>

              <div>

                <strong>
                  Psychology-focused support
                </strong>

                <p>
                  PsyBot provides concise, supportive
                  responses based on psychology-focused
                  knowledge to help you reflect on thoughts,
                  emotions and everyday challenges.
                </p>

              </div>

            </section>

          </>

        ) : (

          /* ==================================================
             CONVERSATION
          ================================================== */

          <section className="conversation-page">

            <div className="conversation-header">

              <div>

                <span className="section-label">
                  PSYBOT CONVERSATION
                </span>

                <h2>
                  Let's explore this together.
                </h2>

              </div>

              <div className="conversation-status">

                <span></span>

                Active

              </div>

            </div>


            {/* CHAT */}

            <section className="chat-container">

              <div className="messages">

                {messages.map((msg, index) => (

                  <div
                    key={index}
                    className={`message-row ${
                      msg.role === "user"
                        ? "user-row"
                        : "bot-row"
                    }`}
                  >

                    <div
                      className={`avatar ${
                        msg.role === "user"
                          ? "user-avatar"
                          : "bot-avatar"
                      }`}
                    >
                      {msg.role === "user"
                        ? "You"
                        : "🧠"}
                    </div>


                    <div
                      className={`message ${
                        msg.role === "user"
                          ? "user-message"
                          : "bot-message"
                      }`}
                    >
                      {msg.content}
                    </div>

                  </div>

                ))}


                {/* TYPING */}

                {loading && (

                  <div className="message-row bot-row">

                    <div className="avatar bot-avatar">
                      🧠
                    </div>

                    <div className="message bot-message typing">

                      <span></span>
                      <span></span>
                      <span></span>

                    </div>

                  </div>

                )}

              </div>

            </section>


            {/* CHAT INPUT */}

            <section className="input-section">

              <div className="input-wrapper">

                <textarea
                  value={message}
                  onChange={(event) =>
                    setMessage(event.target.value)
                  }
                  onKeyDown={handleKeyDown}
                  placeholder="Ask a psychology-related question..."
                  rows="1"
                  disabled={loading}
                />

                <button
                  className="send-button"
                  onClick={() => sendMessage()}
                  disabled={
                    !message.trim() || loading
                  }
                  aria-label="Send message"
                >
                  ↑
                </button>

              </div>

              <p className="input-hint">
                Explore thoughts, emotions, stress,
                relationships and mental well-being.
              </p>

            </section>


            {/* DISCLAIMER */}

            <section className="disclaimer">

              <strong>
                Important
              </strong>

              <span>
                PsyBot provides general psychological
                information and supportive guidance. It
                does not diagnose mental-health conditions
                or replace professional psychological or
                medical care.
              </span>

            </section>

          </section>

        )}

      </main>


      {/* ==================================================
          FOOTER
      ================================================== */}

      <footer className="footer">

        <div className="footer-left">

          <div className="footer-brand">

            <span className="footer-logo">
              🧠
            </span>

            <div>

              <strong>
                PsyBot
              </strong>

              <span>
                Psychology Support Assistant
              </span>

            </div>

          </div>


          <p>
            Designed & developed by{" "}
            <strong>
              Siddhupasa
            </strong>
          </p>

        </div>


        <div className="footer-right">

          <span className="connect-label">
            Connect
          </span>

          <div className="social-links">

            <a
              href="https://www.linkedin.com/in/siddhu-parasa/"
              target="_blank"
              rel="noopener noreferrer"
              className="social-link"
              title="LinkedIn"
            >
              in
            </a>


            <a
              href="https://github.com/siddhuparasa/"
              target="_blank"
              rel="noopener noreferrer"
              className="social-link"
              title="GitHub"
            >
              GH
            </a>


            <a
              href="mailto:siddhuparaasa99@gmail.com"
              className="social-link"
              title="Email"
            >
              @
            </a>


            <a
              href="https://wa.me/919391757059"
              target="_blank"
              rel="noopener noreferrer"
              className="social-link"
              title="WhatsApp"
            >
              WA
            </a>

          </div>

        </div>

      </footer>

    </div>
  );
}

export default App;