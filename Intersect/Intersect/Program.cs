using System;
using System.Collections.Generic;
using System.Linq;

namespace Intersect
{
    class Program
    {
        static void Main(string[] args)
        {
            List<int> list1 = new List<int>();
            List<int> list2 = new List<int>();
            List<int> list3 = new List<int>();

            list1.AddRange(new int[] { 1, 2, 4, 5, 6, 9, 10 });
            list2.AddRange(new int[] { 1, 2, 5, 7, 8, 10, 11 });
            list3.AddRange(new int[] { 2, 3, 6, 7, 9, 10 });

            IEnumerable<int> listCommon = list1.Intersect(list2).Intersect(list3).ToArray();

            foreach (int i in listCommon)
            {
                Console.Write(i + " ");
            }

        }
    }
}
