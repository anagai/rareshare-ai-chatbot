import Link from "next/link";
import Image from "next/image";
import NavBar from "./navbar";
import { FaBots } from "react-icons/fa6";

export default function Header() {
  return (
    <header className="flex items-center p-10">
      <Link href="/" className="text-4xl font-bold mr-auto hover:text-blue-400">
      <Image
          className="dark:invert"
          src="/rareshare.png"
          alt="rareshare logo"
          width={270}
          height={70}
          priority
        />
      </Link>
      <NavBar />
    </header>
  );
}
