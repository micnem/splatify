using System;
using System.Collections.Generic;
// Simple business object. A PartId is used to identify the type of part 
// but the part name can change. 
public class Song : IEquatable<Song>, IComparable<Song>
{
    public string SongName { get; set; }

    public int AffinityVal { get; set; }

    public override string ToString()
    {
        return "Affinity Score: " + AffinityVal + "   Name: " + SongName;
    }
    public override bool Equals(object obj)
    {
        if (obj == null) return false;
        Song objAsPart = obj as Song;
        if (objAsPart == null) return false;
        else return Equals(objAsPart);
    }
    public int SortByNameAscending(string name1, string name2)
    {

        return name1.CompareTo(name2);
    }

    // Default comparer for Part type.
    public int CompareTo(Song comparePart)
    {
        // A null value means that this object is greater.
        if (comparePart == null)
            return 1;

        else
            return this.AffinityVal.CompareTo(comparePart.AffinityVal);
    }
    public override int GetHashCode()
    {
        return AffinityVal;
    }
    public bool Equals(Song other)
    {
        if (other == null) return false;
        return (this.AffinityVal.Equals(other.AffinityVal));
    }
    // Should also override == and != operators.

}
public class Example
{
    public static void Main()
    {
        // Create a list of parts.
        List<Song> song = new List<Song>();

        // Add parts to the list.
        song.Add(new Song() { SongName = "regular bitch", AffinityVal = 1434 });
        song.Add(new Song() { SongName = "crank it", AffinityVal = 1234 });
        song.Add(new Song() { SongName = "shift dope", AffinityVal = 1634 }); ;
        // Name intentionally left null.

        song.Add(new Song() { SongName = "banana seat", AffinityVal = 1444 });
        song.Add(new Song() { SongName = "cassette", AffinityVal = 1534 });


        // Write out the parts in the list. This will call the overridden 
        // ToString method in the Part class.
        Console.WriteLine("\nBefore sort:");
        foreach (Song aPart in song)
        {
            Console.WriteLine(aPart);
        }


        // Call Sort on the list. This will use the 
        // default comparer, which is the Compare method 
        // implemented on Part.
        song.Sort();


        Console.WriteLine("\nAfter sort by affinity value:");
        foreach (Song aPart in song)
        {
            Console.WriteLine(aPart);
        }

        // This shows calling the Sort(Comparison(T) overload using 
        // an anonymous method for the Comparison delegate. 
        // This method treats null as the lesser of two values.
        song.Sort(delegate (Song x, Song y)
        {
            if (x.SongName == null && y.SongName == null) return 0;
            else if (x.SongName == null) return -1;
            else if (y.SongName == null) return 1;
            else return x.SongName.CompareTo(y.SongName);
        });

        Console.WriteLine("\nAfter sort by name:");
        foreach (Song aPart in song)
        {
            Console.WriteLine(aPart);
        }


    }
}