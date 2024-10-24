import Chatbot from "@/components/Chatbot/chatbot";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <section className="mb-40 text-center">
        <h1 className="text-5xl mb-10 text-blue-400">
          RareShare: The Global Platform for Connecting Rare Disease Patients
        </h1>

        <p className="text-xl">
          Rareshare is an unique social hub serving hundreds of rare disorder communities since 2008.
        </p>
      </section>

      <Chatbot />
    </main>
  );
}
