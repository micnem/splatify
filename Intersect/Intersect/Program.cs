using System;
using System.Collections.Generic;
using System.Linq;

namespace Intersect
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> list1 = new List<string>();
            List<string> list2 = new List<string>();
            List<string> list3 = new List<string>();

            list1.AddRange(new string[] { "Alfred Kingsby", "FUB", "Wakky Bakky", "Hilo", "Ridin", "GMFB", "Levy" });
            list2.AddRange(new string[] { "Alfred Kingsby", "Siggy Siggurdson", "FUB", "NOUT", "Bob DillyWally", "GMFB", "HiLo" });
            list3.AddRange(new string[] { "Alfred Kingsby", "FUB", "Wakky Bakky", "Hilo", "Ridin", "GMFB", "Levy" });

            IEnumerable<string> listCommon = list1.Intersect(list2).Intersect(list3).ToArray();

            foreach (string i in listCommon)
            {
                Console.Write(i + " ");
            }

        }
    }
}
