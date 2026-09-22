export const features = [
  { title: "Score a round", detail: "Personal and shared scorecards", action: "Coming next" },
  { title: "Your bag", detail: "Track every physical disc", action: "Coming next" },
  { title: "Flight Lab", detail: "Log and visualize throws", action: "Coming next" }
];

export default function App() {
  return (
    <main>
      <header className="topbar">
        <a className="brand" href="/" aria-label="Disc Golf Tracker home">
          <span className="mark" aria-hidden="true">DGT</span>
          <span>Disc Golf Tracker</span>
        </a>
        <button className="quiet" type="button">Sign in</button>
      </header>

      <section className="hero">
        <p className="eyebrow">Version 0.1 · Foundation</p>
        <h1>Your rounds.<br />Your plastic.<br /><em>Your flight.</em></h1>
        <p className="lede">
          A private, self-hosted home for scores, discs, and the throws that make every round yours.
        </p>
        <button className="primary" type="button">Start a round <span aria-hidden="true">→</span></button>
      </section>

      <section className="feature-grid" aria-label="Application areas">
        {features.map((feature, index) => (
          <article className="feature" key={feature.title}>
            <span className="number">0{index + 1}</span>
            <div>
              <h2>{feature.title}</h2>
              <p>{feature.detail}</p>
            </div>
            <span className="status">{feature.action}</span>
          </article>
        ))}
      </section>

      <footer>
        <span>Built for the course. Owned by you.</span>
        <span>Installable PWA · Offline scoring planned</span>
      </footer>
    </main>
  );
}
